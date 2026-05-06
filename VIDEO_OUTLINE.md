# 5-Minute Video Outline

## Goal

Show that the tool satisfies the crawler, inverted-index, search, testing, and
GenAI reflection requirements. The lessons in `lessons/` can be used as short
teaching notes while preparing the narration.

## 0:00-1:25 Live Demonstration

1. Start the shell:

```shell
uv run python -m src.main
```

2. Run `build --max-pages 3` and explicitly mention the 6 second politeness
   window from the brief.
3. Run `load` to show that the index can be saved and restored.
4. Run `print good` to show the inverted index entry: frequency, positions,
   first position, and density.
5. Run `find indifference` for a single-term query.
6. Run `find good friends` for multi-word AND search.
7. Run `find "good friends"` to show exact phrase matching from stored
   positions.
8. Run `find frends` to show no-result handling and suggestions.

## 1:25-2:45 Component Walkthrough

- `src/crawler.py`: explain `QuoteCrawler`, the URL queue, duplicate prevention,
  internal-link filtering, and `_wait_if_needed`. Use
  `lessons/01-polite-crawling.md` and
  `lessons/02-parsing-and-link-discovery.md`.
- `src/indexer.py`: explain tokenisation, lowercase terms, posting lists,
  `TermStats`, `DocumentInfo`, and JSON save/load. Use
  `lessons/03-inverted-index-construction.md`.
- `src/search.py`: explain query parsing, posting-list intersection, quoted
  phrases, conservative stemming, stop-word handling, suggestions, snippets, and
  TF-IDF-inspired ranking. Use `lessons/04-query-processing-and-ranking.md`.
- `src/main.py`: explain how the shell connects `build`, `load`, `print`, and
  `find`. Use `lessons/05-cli-persistence-and-testing.md`.

## 2:45-3:25 Testing and Evidence

Run or show output from:

```shell
uv run pytest -q
uv run pytest --cov=src --cov-report=term-missing
uv run python benchmarks/benchmark_search.py --repeat 20
```

Mention:

- crawler tests use fake HTTP sessions,
- politeness is tested with fake time and fake sleep,
- indexer tests check frequencies, positions, replacement, and persistence,
- search tests check empty input, missing terms, AND queries, phrases,
  suggestions, stemming, and stop-word handling,
- GitHub Actions runs the tests automatically.

## 3:25-3:45 Version Control

Show:

```shell
git log --oneline --decorate
```

Explain that the work was built incrementally: core crawler, indexer, search,
tests, documentation, and final verification.

## 3:45-5:00 Critical GenAI Evaluation

Declare the tool used: OpenAI Codex/ChatGPT.

Use `lessons/06-critical-genai-usage.md` and make the reflection specific:

- Helpful use: GenAI helped convert the brief into a module plan: crawler,
  indexer, search engine, command shell, tests, and documentation.
- Helpful use: GenAI suggested mocked crawler tests, which avoided slow live
  network tests while still checking politeness.
- Human correction: AI-generated crawler ideas needed checking against the exact
  6 second politeness requirement.
- Human correction: multi-word search needed AND semantics, not a looser OR
  search.
- Human correction: the index needed positions as well as frequencies so exact
  phrase search could be explained and implemented.
- Learning impact: GenAI accelerated scaffolding, but the learning came from
  tracing the data flow and proving each decision against the brief.

Suggested closing line:

"The main lesson from using GenAI was that it is strongest as a planning and
review partner, but it still needs human verification. In this project I used it
to move faster, then checked the result through the brief, tests, and an index
format I can explain."
