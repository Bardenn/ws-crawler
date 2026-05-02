# COMP3011 Search Engine Tool

Python search tool for the COMP3011 Coursework 2 target site:
<https://quotes.toscrape.com/>.

The program crawls pages politely, builds an inverted index, saves it as JSON,
loads it again later, prints posting lists for individual words, and finds pages
that contain every word in a query.

## Features

- Polite breadth-first crawler with a default 6 second delay between requests.
- Inverted index storing frequency, token positions, first position, and density.
- Case-insensitive tokenisation and search.
- Multi-word query support using AND semantics.
- Quoted exact-phrase search, for example `find "good friends"`.
- TF-IDF inspired ranking with an extra bonus for adjacent phrase matches.
- Query suggestions for close misspellings when no pages are found.
- JSON index persistence in `data/index.json`.
- Benchmark script for query timing and index statistics.
- GitHub Actions workflow for automated tests and coverage.
- Unit and end-to-end tests for crawler, indexer, search, and shell behaviour.

## Repository Structure

```text
.
├── src/
│   ├── crawler.py
│   ├── indexer.py
│   ├── search.py
│   └── main.py
├── tests/
│   ├── test_cli_e2e.py
│   ├── test_crawler.py
│   ├── test_indexer.py
│   ├── test_main.py
│   └── test_search.py
├── benchmarks/
│   └── benchmark_search.py
├── .github/workflows/
│   └── tests.yml
├── data/
│   └── index.json
├── AI_USAGE.md
├── VIDEO_OUTLINE.md
├── requirements.txt
└── README.md
```

## Installation

Use Python 3.11 or newer. The recommended setup uses `uv`:

```shell
uv sync
```

If `uv` is not available, use `pip`:

```shell
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Usage

Start the interactive shell:

```shell
uv run python -m src.main
```

Build a fresh index. This crawls the target website and saves to
`data/index.json`.

```shell
> build
```

To keep a demonstration short, crawl fewer pages while still preserving the
required 6 second delay:

```shell
> build --max-pages 3
```

Load an existing index:

```shell
> load
```

Print the inverted index for a word:

```shell
> print nonsense
```

Find pages containing one or more query terms:

```shell
> find indifference
> find good friends
> find "good friends"
```

Unquoted multi-word queries use AND semantics: every term must appear on the
page, but the terms do not have to be adjacent. Quoted phrases require adjacent
positions in the index, so `find "good friends"` is stricter than
`find good friends`.

The shell handles empty queries and missing words gracefully:

```shell
> find
Please provide a non-empty search query.

> print wordthatdoesnotexist
No index entries found for 'wordthatdoesnotexist'.
```

For search queries with a likely typo, the shell suggests close indexed words:

```shell
> find frends
No pages found for 'frends'.
Suggestions:
  frends: friends
```

You can also run one command non-interactively:

```shell
uv run python -m src.main --command "load"
uv run python -m src.main --command "find good friends"
```

## Design Rationale

The index is a dictionary from term to posting list:

```python
{
    "good": {
        "https://quotes.toscrape.com/page/1/": {
            "frequency": 1,
            "positions": [34],
            "first_position": 34,
            "density": 0.01
        }
    }
}
```

This structure makes `print word` a direct dictionary lookup. For `find good
friends`, the search engine intersects the posting-list URL sets so only pages
containing every query term are returned. Ranking then uses term frequency,
inverse document frequency, and a phrase bonus when the terms appear next to
each other.

The crawler separates fetching from indexing. That keeps network error handling
inside `crawler.py`, tokenisation and storage inside `indexer.py`, and query
processing inside `search.py`.

## Complexity and Performance

Let:

- `D` be the number of indexed documents.
- `T` be the number of unique terms.
- `P(t)` be the posting list size for term `t`.
- `Q` be the number of query terms.

Index construction is linear in the number of tokens crawled, because each token
is normalised once and appended to a posting list. A single-word lookup is
approximately `O(1)` for the dictionary lookup plus `O(P(t))` to print results.
For a multi-word query, search intersects posting-list URL sets, which is
approximately `O(P(t1) + ... + P(tQ))`. Exact phrase checks use stored token
positions, so they avoid scanning the original page text.

Run the benchmark script against the saved index:

```shell
uv run python benchmarks/benchmark_search.py --repeat 100
```

The benchmark reports document count, vocabulary size, index load time, and
average/best timings for representative queries.

## Testing

Run the full test suite:

```shell
uv run pytest -q
```

Run with coverage:

```shell
uv run pytest --cov=src --cov-report=term-missing
```

Testing strategy:

- Crawler tests use fake HTTP sessions so tests are fast and deterministic.
- The politeness window is tested with fake `sleep` and `monotonic` functions.
- Indexer tests check tokenisation, frequencies, positions, replacement, and
  JSON persistence.
- Search tests check case-insensitive lookup, multi-word AND queries, empty
  inputs, missing terms, exact quoted phrases, suggestions, and phrase ranking.
- CLI tests check that `load`, `print`, and `find` produce user-facing output.
- End-to-end CLI tests run `python -m src.main` in a subprocess.
- GitHub Actions runs tests and coverage automatically on push and pull request.

## Dependencies

- `requests` for HTTP requests.
- `beautifulsoup4` for HTML parsing.
- `pytest` and `pytest-cov` for testing and coverage.

## Video Demonstration Notes

Use `VIDEO_OUTLINE.md` as a 5-minute script. The video should show:

- `build`, `load`, `print`, and `find`.
- Multi-word queries and edge cases.
- Key data structures and code sections.
- Test suite execution.
- Git commit history.
- The GenAI declaration and critical evaluation from `AI_USAGE.md`.
