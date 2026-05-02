"""Inverted index construction and persistence.

The index stores one posting list per normalised term.  Each posting records
the pages containing the term, its frequency, all token positions, and a few
derived statistics that are useful for ranking and explanation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
import json
import re
from pathlib import Path
from typing import Any


TOKEN_PATTERN = re.compile(r"[a-z0-9]+(?:'[a-z0-9]+)?")


def tokenize(text: str) -> list[str]:
    """Return case-insensitive word tokens from user text or page text."""
    return TOKEN_PATTERN.findall(text.lower())


@dataclass
class TermStats:
    """Statistics for one word on one page."""

    frequency: int
    positions: list[int]
    first_position: int
    density: float

    def to_dict(self) -> dict[str, Any]:
        return {
            "frequency": self.frequency,
            "positions": self.positions,
            "first_position": self.first_position,
            "density": self.density,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "TermStats":
        return cls(
            frequency=int(data["frequency"]),
            positions=[int(position) for position in data["positions"]],
            first_position=int(data["first_position"]),
            density=float(data["density"]),
        )


@dataclass
class DocumentInfo:
    """Metadata retained for a crawled page."""

    url: str
    title: str
    text: str
    token_count: int

    def to_dict(self) -> dict[str, Any]:
        return {
            "url": self.url,
            "title": self.title,
            "text": self.text,
            "token_count": self.token_count,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "DocumentInfo":
        return cls(
            url=str(data["url"]),
            title=str(data.get("title", "")),
            text=str(data.get("text", "")),
            token_count=int(data.get("token_count", 0)),
        )


@dataclass
class InvertedIndex:
    """A serialisable inverted index keyed by normalised words."""

    base_url: str = ""
    terms: dict[str, dict[str, TermStats]] = field(default_factory=dict)
    documents: dict[str, DocumentInfo] = field(default_factory=dict)
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    @property
    def page_count(self) -> int:
        return len(self.documents)

    def add_document(self, url: str, text: str, title: str = "") -> None:
        """Tokenise a page and add or replace its term postings."""
        self.remove_document(url)
        tokens = tokenize(text)
        self.documents[url] = DocumentInfo(
            url=url,
            title=title,
            text=text,
            token_count=len(tokens),
        )

        positions_by_term: dict[str, list[int]] = {}
        for position, term in enumerate(tokens):
            positions_by_term.setdefault(term, []).append(position)

        token_count = max(len(tokens), 1)
        for term, positions in positions_by_term.items():
            postings = self.terms.setdefault(term, {})
            frequency = len(positions)
            postings[url] = TermStats(
                frequency=frequency,
                positions=positions,
                first_position=positions[0],
                density=frequency / token_count,
            )

    def remove_document(self, url: str) -> None:
        """Remove stale postings for a page before re-indexing it."""
        if url not in self.documents:
            return

        del self.documents[url]
        empty_terms: list[str] = []
        for term, postings in self.terms.items():
            postings.pop(url, None)
            if not postings:
                empty_terms.append(term)
        for term in empty_terms:
            del self.terms[term]

    def postings_for(self, term: str) -> dict[str, TermStats]:
        """Return the posting list for a case-insensitive term."""
        tokens = tokenize(term)
        if not tokens:
            return {}
        return self.terms.get(tokens[0], {})

    def to_dict(self) -> dict[str, Any]:
        return {
            "metadata": {
                "base_url": self.base_url,
                "created_at": self.created_at,
                "page_count": self.page_count,
                "term_count": len(self.terms),
            },
            "documents": {
                url: document.to_dict()
                for url, document in sorted(self.documents.items())
            },
            "terms": {
                term: {
                    url: stats.to_dict()
                    for url, stats in sorted(postings.items())
                }
                for term, postings in sorted(self.terms.items())
            },
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "InvertedIndex":
        metadata = data.get("metadata", {})
        index = cls(
            base_url=str(metadata.get("base_url", "")),
            created_at=str(metadata.get("created_at", "")),
        )
        index.documents = {
            url: DocumentInfo.from_dict(document)
            for url, document in data.get("documents", {}).items()
        }
        index.terms = {
            term: {
                url: TermStats.from_dict(stats)
                for url, stats in postings.items()
            }
            for term, postings in data.get("terms", {}).items()
        }
        return index

    def save(self, path: str | Path) -> None:
        destination = Path(path)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(
            json.dumps(self.to_dict(), indent=2, sort_keys=True),
            encoding="utf-8",
        )

    @classmethod
    def load(cls, path: str | Path) -> "InvertedIndex":
        source = Path(path)
        try:
            data = json.loads(source.read_text(encoding="utf-8"))
        except FileNotFoundError as exc:
            raise FileNotFoundError(
                f"No saved index found at {source}. Run 'build' first."
            ) from exc
        except json.JSONDecodeError as exc:
            raise ValueError(f"Index file at {source} is not valid JSON.") from exc
        return cls.from_dict(data)

