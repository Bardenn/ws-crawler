"""Query processing and ranking for the inverted index."""

from __future__ import annotations

from dataclasses import dataclass
from difflib import get_close_matches
import math
import re

from .indexer import InvertedIndex, TermStats, tokenize

QUOTED_PHRASE_PATTERN = re.compile(r'"([^"]+)"')
STOP_WORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "for",
    "from",
    "has",
    "he",
    "in",
    "is",
    "it",
    "its",
    "of",
    "on",
    "or",
    "that",
    "the",
    "to",
    "was",
    "were",
    "with",
    "you",
    "your",
}


@dataclass(frozen=True)
class SearchResult:
    """A ranked search result returned to the CLI."""

    url: str
    title: str
    score: float
    matched_terms: list[str]
    snippet: str


@dataclass(frozen=True)
class Query:
    """Parsed user query containing individual terms and exact phrases."""

    terms: list[str]
    phrases: list[list[str]]

    @property
    def all_terms(self) -> list[str]:
        terms: list[str] = []
        for term in self.terms:
            if term not in terms:
                terms.append(term)
        for phrase in self.phrases:
            for term in phrase:
                if term not in terms:
                    terms.append(term)
        return terms


class SearchEngine:
    """Case-insensitive search over an :class:`InvertedIndex`."""

    def __init__(self, index: InvertedIndex) -> None:
        self.index = index
        self._stem_to_terms: dict[str, list[str]] = {}
        for term in index.terms:
            self._stem_to_terms.setdefault(stem_term(term), []).append(term)

    def print_term(self, word: str) -> dict[str, TermStats]:
        """Return postings for a single word."""
        return self.index.postings_for(word)

    def find(self, query: str, limit: int | None = None) -> list[SearchResult]:
        """Return pages matching every query term and quoted phrase."""
        parsed_query = parse_query(query)
        terms = parsed_query.all_terms
        if not terms:
            return []

        candidate_urls: set[str] | None = None
        for term in parsed_query.terms:
            variants = self._variants_for_term(term)
            if not variants:
                return []
            urls_for_concept = {
                url
                for variant in variants
                for url in self.index.terms.get(variant, {})
            }
            candidate_urls = (
                urls_for_concept
                if candidate_urls is None
                else candidate_urls & urls_for_concept
            )

        for phrase in parsed_query.phrases:
            phrase_postings = [self.index.terms.get(term, {}) for term in phrase]
            if any(not postings for postings in phrase_postings):
                return []
            phrase_urls = set(phrase_postings[0])
            for postings in phrase_postings[1:]:
                phrase_urls &= set(postings)
            phrase_urls = {
                url
                for url in phrase_urls
                if self._count_phrase_occurrences(url, phrase) > 0
            }
            candidate_urls = (
                phrase_urls
                if candidate_urls is None
                else candidate_urls & phrase_urls
            )

        if candidate_urls is None:
            return []

        results = [self._score_document(url, parsed_query) for url in candidate_urls]
        results.sort(key=lambda result: (-result.score, result.url))
        return results if limit is None else results[:limit]

    def suggest_terms(self, query: str, limit: int = 3) -> dict[str, list[str]]:
        """Suggest close indexed terms for query tokens that are not present."""
        suggestions: dict[str, list[str]] = {}
        vocabulary = list(self.index.terms)
        for term in parse_query(query).all_terms:
            if self._variants_for_term(term):
                continue
            matches = get_close_matches(term, vocabulary, n=limit, cutoff=0.72)
            if matches:
                suggestions[term] = matches
        return suggestions

    def _score_document(self, url: str, query: Query) -> SearchResult:
        document = self.index.documents[url]
        score = 0.0
        matched_terms: list[str] = []
        total_docs = max(self.index.page_count, 1)

        for term in query.terms:
            for variant in self._variants_for_term(term):
                stats = self.index.terms[variant].get(url)
                if stats is None:
                    continue
                score += self._tf_idf(stats, variant, total_docs, document.token_count)
                if variant not in matched_terms:
                    matched_terms.append(variant)

        for phrase in query.phrases:
            for term in phrase:
                stats = self.index.terms[term].get(url)
                if stats is None:
                    continue
                score += self._tf_idf(stats, term, total_docs, document.token_count)
                if term not in matched_terms:
                    matched_terms.append(term)

        for phrase in query.phrases:
            phrase_occurrences = self._count_phrase_occurrences(url, phrase)
            score += 3.0 + (0.5 * phrase_occurrences)

        if (
            not query.phrases
            and len(query.terms) > 1
            and all(term in self.index.terms for term in query.terms)
        ):
            phrase_occurrences = self._count_phrase_occurrences(url, query.terms)
            if phrase_occurrences:
                score += 2.0 + (0.25 * phrase_occurrences)

        return SearchResult(
            url=url,
            title=document.title,
            score=round(score, 6),
            matched_terms=matched_terms,
            snippet=self._make_snippet(document.text, query.all_terms),
        )

    def _variants_for_term(self, term: str) -> list[str]:
        variants = self._stem_to_terms.get(stem_term(term), [])
        return sorted(variants, key=lambda variant: (variant != term, variant))

    def _tf_idf(
        self,
        stats: TermStats,
        term: str,
        total_docs: int,
        token_count: int,
    ) -> float:
        document_frequency = len(self.index.terms[term])
        inverse_document_frequency = math.log(
            (1 + total_docs) / (1 + document_frequency)
        ) + 1
        term_frequency = stats.frequency / max(token_count, 1)
        return term_frequency * inverse_document_frequency

    def _count_phrase_occurrences(self, url: str, terms: list[str]) -> int:
        if len(terms) < 2:
            return 0

        first_positions = self.index.terms[terms[0]][url].positions
        other_position_sets = [
            set(self.index.terms[term][url].positions)
            for term in terms[1:]
        ]
        occurrences = 0
        for start in first_positions:
            if all(
                start + offset + 1 in positions
                for offset, positions in enumerate(other_position_sets)
            ):
                occurrences += 1
        return occurrences

    @staticmethod
    def _make_snippet(text: str, terms: list[str], radius: int = 70) -> str:
        if not text:
            return ""

        lower_text = text.lower()
        first_match = min(
            (
                position
                for term in terms
                for position in [lower_text.find(term)]
                if position >= 0
            ),
            default=0,
        )
        start = max(first_match - radius, 0)
        end = min(first_match + radius, len(text))
        snippet = text[start:end].strip()
        snippet = re.sub(r"\s+", " ", snippet)
        if start > 0:
            snippet = f"...{snippet}"
        if end < len(text):
            snippet = f"{snippet}..."
        return snippet


def parse_query(query: str) -> Query:
    """Parse unquoted terms and quoted exact phrases from a user query."""
    phrases = [
        tokenize(match.group(1))
        for match in QUOTED_PHRASE_PATTERN.finditer(query)
        if tokenize(match.group(1))
    ]
    without_phrases = QUOTED_PHRASE_PATTERN.sub(" ", query)
    terms = _remove_stop_words(tokenize(without_phrases))
    return Query(terms=terms, phrases=phrases)


def stem_term(term: str) -> str:
    """Return a conservative stem for query expansion.

    This is deliberately small and dependency-free.  The index still stores the
    original words; stemming is used only to expand unquoted query terms to close
    vocabulary variants such as ``friend`` and ``friends``.
    """
    if len(term) <= 3:
        return term
    if len(term) > 4 and term.endswith("ies"):
        return f"{term[:-3]}y"
    if len(term) > 5 and term.endswith("ing"):
        stem = term[:-3]
        if len(stem) > 2 and stem[-1] == stem[-2]:
            stem = stem[:-1]
        return stem
    if len(term) > 4 and term.endswith("ed"):
        return term[:-2]
    if term.endswith("s") and not term.endswith("ss"):
        return term[:-1]
    return term


def _remove_stop_words(tokens: list[str]) -> list[str]:
    filtered = [token for token in tokens if token not in STOP_WORDS]
    return filtered or tokens
