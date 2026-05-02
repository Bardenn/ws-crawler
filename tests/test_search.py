from src.indexer import InvertedIndex
from src.search import SearchEngine, parse_query


def make_index() -> InvertedIndex:
    index = InvertedIndex()
    index.add_document(
        "https://quotes.toscrape.com/page/1/",
        "Good friends, good books, and a sleepy conscience.",
        "Page 1",
    )
    index.add_document(
        "https://quotes.toscrape.com/page/2/",
        "Friends can make ordinary days good.",
        "Page 2",
    )
    index.add_document(
        "https://quotes.toscrape.com/page/3/",
        "Indifference is a quiet danger.",
        "Page 3",
    )
    return index


def test_print_term_returns_case_insensitive_postings() -> None:
    engine = SearchEngine(make_index())

    postings = engine.print_term("GOOD")

    assert set(postings) == {
        "https://quotes.toscrape.com/page/1/",
        "https://quotes.toscrape.com/page/2/",
    }


def test_find_requires_all_query_terms_for_multi_word_queries() -> None:
    engine = SearchEngine(make_index())

    results = engine.find("good friends")

    assert [result.url for result in results] == [
        "https://quotes.toscrape.com/page/1/",
        "https://quotes.toscrape.com/page/2/",
    ]
    assert all(result.matched_terms == ["good", "friends"] for result in results)


def test_adjacent_phrase_match_receives_ranking_bonus() -> None:
    index = InvertedIndex()
    index.add_document("https://example.test/a/", "good friends are rare", "A")
    index.add_document("https://example.test/b/", "good books and loyal friends", "B")
    engine = SearchEngine(index)

    results = engine.find("good friends")

    assert results[0].url == "https://example.test/a/"
    assert results[0].score > results[1].score


def test_find_handles_empty_and_missing_queries() -> None:
    engine = SearchEngine(make_index())

    assert engine.find("") == []
    assert engine.find("wordthatdoesnotexist") == []
    assert engine.find("good wordthatdoesnotexist") == []


def test_find_can_limit_results_and_handles_empty_document_text() -> None:
    index = InvertedIndex()
    index.add_document("https://example.test/a/", "common term", "A")
    index.add_document("https://example.test/b/", "common term", "B")
    index.add_document("https://example.test/c/", "", "C")
    engine = SearchEngine(index)

    assert len(engine.find("common", limit=1)) == 1
    assert engine._make_snippet("", ["common"]) == ""


def test_parse_query_separates_terms_and_quoted_phrases() -> None:
    query = parse_query('good "loyal friends" books')

    assert query.terms == ["good", "books"]
    assert query.phrases == [["loyal", "friends"]]
    assert query.all_terms == ["good", "books", "loyal", "friends"]


def test_quoted_phrase_requires_adjacent_terms() -> None:
    index = InvertedIndex()
    index.add_document("https://example.test/a/", "good loyal friends stay", "A")
    index.add_document("https://example.test/b/", "good loyal and patient friends", "B")
    engine = SearchEngine(index)

    results = engine.find('"loyal friends"')

    assert [result.url for result in results] == ["https://example.test/a/"]


def test_suggest_terms_returns_close_indexed_words() -> None:
    engine = SearchEngine(make_index())

    suggestions = engine.suggest_terms("frends")

    assert suggestions["frends"] == ["friends"]
