from pathlib import Path

import pytest

from src.indexer import InvertedIndex, tokenize


def test_tokenize_is_case_insensitive_and_ignores_punctuation() -> None:
    assert tokenize("Good, GOOD! friend's 42") == ["good", "good", "friend's", "42"]


def test_add_document_stores_frequency_positions_and_density() -> None:
    index = InvertedIndex(base_url="https://quotes.toscrape.com/")

    index.add_document(
        "https://quotes.toscrape.com/page/1/",
        "Good friends are good company.",
        "Example page",
    )

    postings = index.postings_for("GOOD")
    stats = postings["https://quotes.toscrape.com/page/1/"]

    assert stats.frequency == 2
    assert stats.positions == [0, 3]
    assert stats.first_position == 0
    assert stats.density == 2 / 5
    assert index.documents["https://quotes.toscrape.com/page/1/"].title == "Example page"


def test_reindexing_same_url_replaces_stale_postings() -> None:
    index = InvertedIndex()

    index.add_document("https://example.test/", "old word")
    index.add_document("https://example.test/", "new word")

    assert index.postings_for("old") == {}
    assert "https://example.test/" in index.postings_for("new")
    assert index.page_count == 1


def test_save_and_load_round_trip(tmp_path: Path) -> None:
    path = tmp_path / "index.json"
    index = InvertedIndex(base_url="https://quotes.toscrape.com/")
    index.add_document("https://quotes.toscrape.com/", "Truth is beautiful.", "Quotes")

    index.save(path)
    loaded = InvertedIndex.load(path)

    assert loaded.base_url == "https://quotes.toscrape.com/"
    assert loaded.page_count == 1
    assert loaded.postings_for("truth")["https://quotes.toscrape.com/"].positions == [0]


def test_load_reports_missing_and_invalid_index_files(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError, match="Run 'build' first"):
        InvertedIndex.load(tmp_path / "missing.json")

    invalid_path = tmp_path / "invalid.json"
    invalid_path.write_text("{not json", encoding="utf-8")

    with pytest.raises(ValueError, match="not valid JSON"):
        InvertedIndex.load(invalid_path)
