# Lesson 3: Inverted Index Construction

## What This Component Does

The indexer converts crawled page text into an inverted index. Instead of storing
only a list of pages, the tool stores a dictionary from each word to the pages
where it appears.

Conceptually:

```python
{
    "good": {
        "https://quotes.toscrape.com/": {
            "frequency": 2,
            "positions": [15, 48],
            "first_position": 15,
            "density": 0.02
        }
    }
}
```

This structure directly supports the coursework commands:

- `print good` is a dictionary lookup.
- `find good friends` intersects the pages for `good` and `friends`.
- exact phrase search can use stored token positions.

## Current Design

The indexer has three main data objects:

- `TermStats`: statistics for one term on one page.
- `DocumentInfo`: metadata for one crawled document.
- `InvertedIndex`: the full serialisable index.

When a document is added, the text is tokenised in lowercase. The indexer records
every token position. It then groups positions by term and calculates:

- frequency: how many times the word appears on the page,
- positions: where the word appears in token order,
- first position: the earliest occurrence,
- density: frequency divided by total token count.

## Tokenisation

The tokenizer uses a regular expression that keeps lowercase words, numbers, and
simple apostrophe words. This makes search case-insensitive and avoids treating
punctuation as part of words.

For example:

- `Good` becomes `good`.
- `friends.` becomes `friends`.
- `don't` remains one token.

The brief says search is not case sensitive, so this is a required design
choice, not just a convenience.

## Re-indexing a Page

Before adding a document, the index removes any previous postings for the same
URL. This prevents duplicate statistics if the same page is indexed again.

That detail is worth mentioning because AI-generated implementations often
append new postings without handling replacement. The result can silently double
frequencies and corrupt search ranking.

## Persistence

The index saves to JSON. This keeps the submitted `data/index.json` readable and
easy to inspect in the video. It also means `load` can reconstruct the dataclass
objects from plain dictionaries.

## Pros and Cons of Different Approaches

### Dictionary-Based Inverted Index

Pros:

- Fast lookup for individual words.
- Simple to print and explain.
- Natural fit for JSON persistence.

Cons:

- Can use a lot of memory for large websites.
- Needs care when serialising dataclass objects.

### Forward Index Only

Pros:

- Simple: each page stores its own words.
- Easy to build while crawling.

Cons:

- Slow search, because every page must be scanned for every query.
- Does not demonstrate the key search engine mechanism as well.

### Store Frequencies Only

Pros:

- Smaller index.
- Enough for basic keyword search and simple ranking.

Cons:

- Cannot support exact phrase search efficiently.
- Loses explanation value around word positions.

### Store Frequencies and Positions

Pros:

- Supports phrase search.
- Supports richer ranking and snippets.
- Meets the brief's request for occurrence statistics.

Cons:

- Larger index file.
- Slightly more complex to build and explain.
