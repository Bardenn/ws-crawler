# 5-Minute Video Outline

## 0:00-2:00 Live Demonstration

1. Open the terminal and run `uv run python -m src.main`.
2. Run `build --max-pages 3` and point out the 6 second politeness delay.
3. Run `load`.
4. Run `print good`.
5. Run `find indifference`.
6. Run `find good friends`.
7. Run `find "good friends"` to show exact phrase search.
8. Show edge cases: `find`, `find frends`, and `print wordthatdoesnotexist`.

## 2:00-3:30 Code Walkthrough

- `src/crawler.py`: breadth-first crawling, internal-link filtering, error
  handling, and `_wait_if_needed`.
- `src/indexer.py`: tokenisation, inverted-index dictionary, frequency,
  positions, first position, density, and JSON save/load.
- `src/search.py`: posting-list intersection, case-insensitive query
  processing, exact phrases, suggestions, TF-IDF inspired ranking, and phrase
  bonus.
- `src/main.py`: command shell and graceful user messages.
- `benchmarks/benchmark_search.py`: query timing and index statistics.

## 3:30-4:00 Testing

Run:

```shell
uv run pytest -q
uv run pytest --cov=src --cov-report=term-missing
uv run python benchmarks/benchmark_search.py --repeat 20
```

Mention that network calls are mocked, and that politeness is tested with fake
time so tests remain fast. Point out that GitHub Actions runs the same test
suite automatically.

## 4:00-4:30 Version Control

Show:

```shell
git log --oneline --decorate
```

Explain the incremental workflow: core implementation, tests, documentation,
and final verification.

## 4:30-5:00 GenAI Critical Evaluation

Declare OpenAI Codex/ChatGPT usage. Discuss one benefit and one limitation:

- Benefit: faster scaffolding and test ideas.
- Limitation: AI output still needed careful checking against the 6 second
  politeness rule and the exact multi-word query semantics.
