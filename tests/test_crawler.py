from __future__ import annotations

import requests
import pytest

from src.crawler import CrawlError, QuoteCrawler


class FakeResponse:
    def __init__(
        self,
        text: str,
        url: str,
        status_code: int = 200,
        content_type: str = "text/html",
    ) -> None:
        self.text = text
        self.url = url
        self.status_code = status_code
        self.headers = {"content-type": content_type}

    def raise_for_status(self) -> None:
        if self.status_code >= 400:
            raise requests.HTTPError(f"{self.status_code} error")


class FakeSession:
    def __init__(self, responses: dict[str, FakeResponse]) -> None:
        self.responses = responses
        self.headers: dict[str, str] = {}
        self.requested_urls: list[str] = []

    def get(self, url: str, timeout: float) -> FakeResponse:
        self.requested_urls.append(url)
        response = self.responses[url]
        if isinstance(response, Exception):
            raise response
        return response


def test_parse_page_extracts_text_title_and_internal_links() -> None:
    html = """
    <html>
      <head><title>Quotes page</title><script>ignored()</script></head>
      <body>
        <p>First quote</p>
        <a href="/page/2/">next</a>
        <a href="https://other.example/">external</a>
        <a href="/static/app.css">asset</a>
      </body>
    </html>
    """
    crawler = QuoteCrawler(base_url="https://quotes.toscrape.com/", politeness_delay=0)

    page = crawler.parse_page(html, "https://quotes.toscrape.com/")

    assert page.title == "Quotes page"
    assert "First quote" in page.text
    assert "ignored" not in page.text
    assert page.links == ["https://quotes.toscrape.com/page/2/"]


def test_fetch_observes_politeness_window_between_requests() -> None:
    html = "<html><body>quote</body></html>"
    session = FakeSession(
        {
            "https://quotes.toscrape.com/": FakeResponse(
                html, "https://quotes.toscrape.com/"
            ),
            "https://quotes.toscrape.com/page/2/": FakeResponse(
                html, "https://quotes.toscrape.com/page/2/"
            ),
        }
    )
    current_time = [0.0]
    sleeps: list[float] = []

    def sleep(seconds: float) -> None:
        sleeps.append(seconds)
        current_time[0] += seconds

    crawler = QuoteCrawler(
        politeness_delay=6.0,
        session=session,
        sleep_fn=sleep,
        monotonic_fn=lambda: current_time[0],
    )

    crawler.fetch("https://quotes.toscrape.com/")
    crawler.fetch("https://quotes.toscrape.com/page/2/")

    assert sleeps == [6.0]


def test_fetch_respects_robots_crawl_delay_when_larger() -> None:
    html = "<html><body>quote</body></html>"
    session = FakeSession(
        {
            "https://quotes.toscrape.com/robots.txt": FakeResponse(
                "User-agent: *\nCrawl-delay: 10",
                "https://quotes.toscrape.com/robots.txt",
                content_type="text/plain",
            ),
            "https://quotes.toscrape.com/": FakeResponse(
                html, "https://quotes.toscrape.com/"
            ),
            "https://quotes.toscrape.com/page/2/": FakeResponse(
                html, "https://quotes.toscrape.com/page/2/"
            ),
        }
    )
    current_time = [0.0]
    sleeps: list[float] = []

    def sleep(seconds: float) -> None:
        sleeps.append(seconds)
        current_time[0] += seconds

    crawler = QuoteCrawler(
        politeness_delay=6.0,
        session=session,
        sleep_fn=sleep,
        monotonic_fn=lambda: current_time[0],
    )

    crawler.fetch("https://quotes.toscrape.com/")
    crawler.fetch("https://quotes.toscrape.com/page/2/")

    assert sleeps == [10.0, 10.0]


def test_crawl_visits_internal_pages_breadth_first() -> None:
    session = FakeSession(
        {
            "https://quotes.toscrape.com/robots.txt": FakeResponse(
                "User-agent: *\nAllow: /",
                "https://quotes.toscrape.com/robots.txt",
                content_type="text/plain",
            ),
            "https://quotes.toscrape.com/": FakeResponse(
                '<a href="/page/2/">next</a><p>home</p>',
                "https://quotes.toscrape.com/",
            ),
            "https://quotes.toscrape.com/page/2/": FakeResponse(
                '<a href="/page/3/">next</a><p>second</p>',
                "https://quotes.toscrape.com/page/2/",
            ),
            "https://quotes.toscrape.com/page/3/": FakeResponse(
                "<p>third</p>",
                "https://quotes.toscrape.com/page/3/",
            ),
        }
    )
    crawler = QuoteCrawler(politeness_delay=0, max_pages=3, session=session)

    pages = crawler.crawl()

    assert [page.url for page in pages] == [
        "https://quotes.toscrape.com/",
        "https://quotes.toscrape.com/page/2/",
        "https://quotes.toscrape.com/page/3/",
    ]


def test_crawl_skips_pages_blocked_by_robots_txt() -> None:
    session = FakeSession(
        {
            "https://quotes.toscrape.com/robots.txt": FakeResponse(
                "User-agent: *\nDisallow: /page/2/",
                "https://quotes.toscrape.com/robots.txt",
                content_type="text/plain",
            ),
            "https://quotes.toscrape.com/": FakeResponse(
                '<a href="/page/2/">blocked</a><p>home</p>',
                "https://quotes.toscrape.com/",
            ),
            "https://quotes.toscrape.com/page/2/": FakeResponse(
                "<p>should not be fetched</p>",
                "https://quotes.toscrape.com/page/2/",
            ),
        }
    )
    crawler = QuoteCrawler(politeness_delay=0, max_pages=2, session=session)

    pages = crawler.crawl()

    assert [page.url for page in pages] == ["https://quotes.toscrape.com/"]
    assert "https://quotes.toscrape.com/page/2/" not in session.requested_urls


def test_fetch_rejects_page_blocked_by_robots_txt() -> None:
    session = FakeSession(
        {
            "https://quotes.toscrape.com/robots.txt": FakeResponse(
                "User-agent: *\nDisallow: /private/",
                "https://quotes.toscrape.com/robots.txt",
                content_type="text/plain",
            ),
            "https://quotes.toscrape.com/private/": FakeResponse(
                "<p>private</p>",
                "https://quotes.toscrape.com/private/",
            ),
        }
    )
    crawler = QuoteCrawler(politeness_delay=0, session=session)

    with pytest.raises(requests.RequestException, match="robots.txt"):
        crawler.fetch("https://quotes.toscrape.com/private/")

    assert "https://quotes.toscrape.com/private/" not in session.requested_urls


def test_crawl_raises_helpful_error_when_first_page_fails() -> None:
    session = FakeSession(
        {
            "https://quotes.toscrape.com/": requests.ConnectionError("offline"),
        }
    )
    crawler = QuoteCrawler(politeness_delay=0, session=session)

    with pytest.raises(CrawlError, match="Could not crawl"):
        crawler.crawl()


def test_constructor_rejects_invalid_delay_and_page_limit() -> None:
    with pytest.raises(ValueError, match="politeness_delay"):
        QuoteCrawler(politeness_delay=-1)

    with pytest.raises(ValueError, match="max_pages"):
        QuoteCrawler(max_pages=0)


def test_fetch_rejects_non_html_responses() -> None:
    session = FakeSession(
        {
            "https://quotes.toscrape.com/": FakeResponse(
                "body",
                "https://quotes.toscrape.com/",
                content_type="application/json",
            ),
        }
    )
    crawler = QuoteCrawler(politeness_delay=0, session=session)

    with pytest.raises(requests.RequestException, match="non-HTML"):
        crawler.fetch("https://quotes.toscrape.com/")
