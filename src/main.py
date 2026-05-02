"""Command-line shell for the coursework search tool."""

from __future__ import annotations

import argparse
import cmd
from pathlib import Path
import shlex
import sys

from .crawler import CrawlError, QuoteCrawler
from .indexer import InvertedIndex, TermStats, tokenize
from .search import SearchEngine


DEFAULT_INDEX_PATH = Path("data/index.json")
DEFAULT_BASE_URL = "https://quotes.toscrape.com/"


class SearchShell(cmd.Cmd):
    intro = "Quote search shell. Type help or ? to list commands."
    prompt = "> "

    def __init__(
        self,
        index_path: Path = DEFAULT_INDEX_PATH,
        base_url: str = DEFAULT_BASE_URL,
        politeness_delay: float = 6.0,
        max_pages: int = 50,
    ) -> None:
        super().__init__()
        self.index_path = index_path
        self.base_url = base_url
        self.politeness_delay = politeness_delay
        self.max_pages = max_pages
        self.index: InvertedIndex | None = None
        self.engine: SearchEngine | None = None

    def do_build(self, arg: str) -> None:
        """build [--max-pages N] [--output PATH]: crawl, index, and save."""
        try:
            args = _parse_build_args(arg, self.max_pages, self.index_path)
        except SystemExit:
            return

        crawler = QuoteCrawler(
            base_url=self.base_url,
            politeness_delay=self.politeness_delay,
            max_pages=args.max_pages,
        )
        print(
            f"Crawling up to {args.max_pages} pages from {self.base_url} "
            f"with a {self.politeness_delay:.1f}s politeness delay."
        )
        try:
            pages = crawler.crawl()
        except CrawlError as exc:
            print(f"Build failed: {exc}")
            return

        index = InvertedIndex(base_url=self.base_url)
        for page in pages:
            index.add_document(page.url, page.text, page.title)
        index.save(args.output)

        self.index_path = args.output
        self.index = index
        self.engine = SearchEngine(index)
        print(
            f"Built index for {index.page_count} pages and {len(index.terms)} "
            f"unique terms. Saved to {args.output}."
        )

    def do_load(self, arg: str) -> None:
        """load [PATH]: load a saved index from disk."""
        path = Path(arg.strip() or self.index_path)
        try:
            self.index = InvertedIndex.load(path)
        except (FileNotFoundError, ValueError) as exc:
            print(exc)
            return

        self.index_path = path
        self.engine = SearchEngine(self.index)
        print(
            f"Loaded index with {self.index.page_count} pages and "
            f"{len(self.index.terms)} unique terms from {path}."
        )

    def do_print(self, arg: str) -> None:
        """print WORD: show the posting list for one word."""
        engine = self._require_engine()
        if engine is None:
            return

        tokens = tokenize(arg)
        if len(tokens) != 1:
            print("Please provide exactly one word, for example: print nonsense")
            return

        postings = engine.print_term(tokens[0])
        if not postings:
            print(f"No index entries found for '{tokens[0]}'.")
            return

        print(f"Inverted index for '{tokens[0]}':")
        for url, stats in sorted(postings.items()):
            print(f"- {url}")
            print(_format_stats(stats))

    def do_find(self, arg: str) -> None:
        """find QUERY: find pages containing every query term."""
        engine = self._require_engine()
        if engine is None:
            return

        query = arg.strip()
        if not tokenize(query):
            print("Please provide a non-empty search query.")
            return

        results = engine.find(query)
        if not results:
            print(f"No pages found for '{query}'.")
            suggestions = engine.suggest_terms(query)
            if suggestions:
                print("Suggestions:")
                for term, matches in suggestions.items():
                    print(f"  {term}: {', '.join(matches)}")
            return

        print(f"Found {len(results)} page(s) for '{query}':")
        for rank, result in enumerate(results, start=1):
            title = f" ({result.title})" if result.title else ""
            print(f"{rank}. {result.url}{title}")
            print(f"   score={result.score:.6f}; terms={', '.join(result.matched_terms)}")
            if result.snippet:
                print(f"   {result.snippet}")

    def do_exit(self, arg: str) -> bool:
        """exit: leave the shell."""
        return True

    def do_quit(self, arg: str) -> bool:
        """quit: leave the shell."""
        return True

    def emptyline(self) -> None:
        return None

    def _require_engine(self) -> SearchEngine | None:
        if self.engine is None:
            print("No index loaded. Run 'build' or 'load' first.")
            return None
        return self.engine


def _format_stats(stats: TermStats) -> str:
    return (
        f"  frequency={stats.frequency}; first_position={stats.first_position}; "
        f"density={stats.density:.4f}; positions={stats.positions}"
    )


def _parse_build_args(arg: str, default_max_pages: int, default_output: Path) -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="build", add_help=False)
    parser.add_argument("--max-pages", type=int, default=default_max_pages)
    parser.add_argument("--output", type=Path, default=default_output)
    return parser.parse_args(shlex.split(arg))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="COMP3011 quote search tool")
    parser.add_argument("--index", type=Path, default=DEFAULT_INDEX_PATH)
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--max-pages", type=int, default=50)
    parser.add_argument("--delay", type=float, default=6.0)
    parser.add_argument(
        "--command",
        help="Run one shell command non-interactively, e.g. \"load\" or \"find good\".",
    )
    args = parser.parse_args(argv)

    if args.delay < 6.0 and args.base_url == DEFAULT_BASE_URL:
        parser.error("The target website requires a politeness delay of at least 6 seconds.")

    shell = SearchShell(
        index_path=args.index,
        base_url=args.base_url,
        politeness_delay=args.delay,
        max_pages=args.max_pages,
    )
    if args.command:
        command_name = shlex.split(args.command)[0] if shlex.split(args.command) else ""
        if command_name in {"find", "print"} and args.index.exists():
            shell.do_load(str(args.index))
        shell.onecmd(args.command)
        return 0
    shell.cmdloop()
    return 0


if __name__ == "__main__":
    sys.exit(main())
