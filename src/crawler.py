"""Polite crawler for https://quotes.toscrape.com/."""

from __future__ import annotations

from dataclasses import dataclass
import heapq
import time
from typing import Callable
from urllib import robotparser
from urllib.parse import urldefrag, urljoin, urlparse

from bs4 import BeautifulSoup
import requests


@dataclass(frozen=True)
class CrawledPage:
    """A parsed page returned by the crawler."""

    url: str
    title: str
    text: str
    links: list[str]


class CrawlError(RuntimeError):
    """Raised when the starting page cannot be fetched."""


class QuoteCrawler:
    """Breadth-first crawler with a configurable politeness window."""

    def __init__(
        self,
        base_url: str = "https://quotes.toscrape.com/",
        politeness_delay: float = 6.0,
        max_pages: int = 50,
        timeout: float = 10.0,
        session: requests.Session | None = None,
        sleep_fn: Callable[[float], None] = time.sleep,
        monotonic_fn: Callable[[], float] = time.monotonic,
    ) -> None:
        if politeness_delay < 0:
            raise ValueError("politeness_delay cannot be negative")
        if max_pages < 1:
            raise ValueError("max_pages must be at least 1")

        self.base_url = self._normalise_url(base_url)
        self.politeness_delay = politeness_delay
        self.max_pages = max_pages
        self.timeout = timeout
        self.session = session or requests.Session()
        self.sleep_fn = sleep_fn
        self.monotonic_fn = monotonic_fn
        self._last_request_time: float | None = None
        self._base_netloc = urlparse(self.base_url).netloc
        self._robots_parser: robotparser.RobotFileParser | None = None
        self.session.headers.update(
            {
                "User-Agent": (
                    "COMP3011-search-tool/1.0 "
                    "(student coursework crawler; polite delay enabled)"
                )
            }
        )

    def crawl(self) -> list[CrawledPage]:
        """Crawl internal pages from the base URL using breadth-first order."""
        queue: list[tuple[int, int, str]] = []
        sequence = 0
        heapq.heappush(queue, (self._link_priority(self.base_url), sequence, self.base_url))
        queued: set[str] = {self.base_url}
        visited: set[str] = set()
        pages: list[CrawledPage] = []
        first_error: Exception | None = None

        while queue and len(pages) < self.max_pages:
            _, _, url = heapq.heappop(queue)
            queued.discard(url)
            if url in visited:
                continue
            visited.add(url)
            if not self.is_allowed_by_robots(url):
                if not pages and first_error is None:
                    first_error = requests.RequestException(
                        f"Blocked by robots.txt: {url}"
                    )
                continue

            try:
                page = self.fetch(url)
            except requests.RequestException as exc:
                if not pages and first_error is None:
                    first_error = exc
                continue

            pages.append(page)
            for link in page.links:
                if link not in visited and link not in queued:
                    sequence += 1
                    heapq.heappush(queue, (self._link_priority(link), sequence, link))
                    queued.add(link)

        if not pages and first_error is not None:
            raise CrawlError(f"Could not crawl {self.base_url}: {first_error}")
        return pages

    def fetch(self, url: str) -> CrawledPage:
        """Fetch one page while observing the politeness delay."""
        if not self.is_allowed_by_robots(url):
            raise requests.RequestException(f"Blocked by robots.txt: {url}")
        self._wait_if_needed()
        response = self.session.get(url, timeout=self.timeout)
        self._last_request_time = self.monotonic_fn()
        response.raise_for_status()
        content_type = response.headers.get("content-type", "")
        if content_type and "html" not in content_type.lower():
            raise requests.RequestException(f"Skipping non-HTML page: {url}")
        return self.parse_page(response.text, response.url)

    def parse_page(self, html: str, url: str) -> CrawledPage:
        """Extract searchable text, a page title, and internal links."""
        canonical_url = self._normalise_url(url)
        soup = BeautifulSoup(html, "html.parser")
        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()

        title_tag = soup.find("title")
        title = title_tag.get_text(" ", strip=True) if title_tag else canonical_url
        text = soup.get_text(" ", strip=True)

        links: list[str] = []
        seen_links: set[str] = set()
        for anchor in soup.find_all("a", href=True):
            absolute = self._normalise_url(urljoin(canonical_url, anchor["href"]))
            if self._is_internal_html_url(absolute) and absolute not in seen_links:
                seen_links.add(absolute)
                links.append(absolute)

        return CrawledPage(
            url=canonical_url,
            title=title,
            text=text,
            links=sorted(links, key=self._link_priority),
        )

    def is_allowed_by_robots(self, url: str) -> bool:
        """Return whether robots.txt permits this crawler to fetch the URL."""
        parser = self._get_robots_parser()
        user_agent = self.session.headers.get("User-Agent", "*")
        return parser.can_fetch(user_agent, url)

    def _get_robots_parser(self) -> robotparser.RobotFileParser:
        if self._robots_parser is not None:
            return self._robots_parser

        robots_url = urljoin(self.base_url, "/robots.txt")
        parser = robotparser.RobotFileParser(robots_url)
        try:
            self._wait_if_needed()
            response = self.session.get(robots_url, timeout=self.timeout)
            self._last_request_time = self.monotonic_fn()
            if response.status_code in {401, 403}:
                parser.disallow_all = True
            elif 400 <= response.status_code < 500:
                parser.parse([])
            else:
                response.raise_for_status()
                parser.parse(response.text.splitlines())
        except Exception:
            # Be conservative about crawler reliability: if robots.txt cannot be
            # retrieved or parsed, continue as though no rules were published.
            parser.parse([])

        self._robots_parser = parser
        return parser

    def _wait_if_needed(self) -> None:
        if self._last_request_time is None:
            return
        elapsed = self.monotonic_fn() - self._last_request_time
        remaining = self._effective_politeness_delay() - elapsed
        if remaining > 0:
            self.sleep_fn(remaining)

    def _effective_politeness_delay(self) -> float:
        delay = self.politeness_delay
        if self._robots_parser is not None:
            user_agent = self.session.headers.get("User-Agent", "*")
            crawl_delay = self._robots_parser.crawl_delay(user_agent)
            if crawl_delay is not None:
                delay = max(delay, float(crawl_delay))
        return delay

    def _is_internal_html_url(self, url: str) -> bool:
        parsed = urlparse(url)
        if parsed.scheme not in {"http", "https"}:
            return False
        if parsed.netloc != self._base_netloc:
            return False
        path = parsed.path.lower()
        if path in {"/login/", "/logout/"}:
            return False
        return not path.endswith((".jpg", ".jpeg", ".png", ".gif", ".css", ".js"))

    @staticmethod
    def _link_priority(url: str) -> int:
        path = urlparse(url).path
        if path == "/" or path.startswith("/page/"):
            return 0
        if path.startswith("/tag/"):
            return 1
        if path.startswith("/author/"):
            return 2
        return 3

    @staticmethod
    def _normalise_url(url: str) -> str:
        without_fragment = urldefrag(url)[0]
        parsed = urlparse(without_fragment)
        path = parsed.path or "/"
        if path == "/page/1/":
            path = "/"
        if not path.endswith("/") and "." not in path.rsplit("/", maxsplit=1)[-1]:
            path = f"{path}/"
        return parsed._replace(path=path, query="").geturl()
