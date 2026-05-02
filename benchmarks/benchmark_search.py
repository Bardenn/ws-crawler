"""Small benchmark for indexing and query processing.

This is intentionally lightweight so it can be run during a video demonstration
without crawling the live website.  It measures saved-index load time, query
latency, vocabulary size, and document count.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from statistics import mean
import sys
from time import perf_counter

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.indexer import InvertedIndex
from src.search import SearchEngine


DEFAULT_QUERIES = [
    "good friends",
    '"good friends"',
    "indifference",
    "life love",
    "wordthatdoesnotexist",
]


def benchmark(index_path: Path, queries: list[str], repeats: int) -> None:
    start = perf_counter()
    index = InvertedIndex.load(index_path)
    load_seconds = perf_counter() - start
    engine = SearchEngine(index)

    print(f"Index: {index_path}")
    print(f"Documents: {index.page_count}")
    print(f"Unique terms: {len(index.terms)}")
    print(f"Load time: {load_seconds:.6f}s")
    print()
    print("Query timings")
    print("-------------")

    for query in queries:
        timings: list[float] = []
        result_count = 0
        for _ in range(repeats):
            start = perf_counter()
            results = engine.find(query)
            timings.append(perf_counter() - start)
            result_count = len(results)
        print(
            f"{query!r}: results={result_count}, "
            f"avg={mean(timings):.6f}s, best={min(timings):.6f}s"
        )


def main() -> int:
    parser = argparse.ArgumentParser(description="Benchmark saved index search speed")
    parser.add_argument("--index", type=Path, default=Path("data/index.json"))
    parser.add_argument("--repeat", type=int, default=100)
    parser.add_argument("queries", nargs="*", default=DEFAULT_QUERIES)
    args = parser.parse_args()

    benchmark(args.index, args.queries, args.repeat)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
