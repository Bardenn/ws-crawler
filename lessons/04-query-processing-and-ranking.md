# Lesson 4: Query Processing and Ranking

## What This Component Does

The search component takes a user query and returns pages from the inverted
index. It must support:

- case-insensitive lookup,
- single-word queries,
- multi-word queries,
- quoted exact phrase queries,
- ranking so better matches appear first.

## Current Design

`SearchEngine` wraps an `InvertedIndex`. For a normal query such as
`good friends`, it:

1. tokenises the query,
2. removes common stop words when useful,
3. expands terms using conservative stemming,
4. gets the posting list for each term,
5. intersects the URL sets so every term must be present,
6. scores and sorts the matching pages.

For a quoted query such as `"good friends"`, it also checks token positions to
ensure the words are adjacent on the page.

## AND Semantics

The coursework examples imply that `find good friends` should return pages that
contain both words. The implementation uses AND semantics by intersecting posting
lists.

This is an important critical AI point. A common AI-generated shortcut is OR
semantics, where pages containing either `good` or `friends` are returned. That
may produce more results, but it is less precise and does not demonstrate proper
posting-list intersection.

## Exact Phrase Search

Positions make phrase search possible without scanning the original page text.
For `"good friends"`, the engine checks whether a position for `friends` appears
immediately after a position for `good` on the same URL.

This is why the index stores more than just frequencies. The extra data has a
clear user-facing benefit.

## Ranking

Ranking uses a TF-IDF-inspired score:

- term frequency rewards words that appear more often in the document,
- inverse document frequency rewards rarer query words,
- phrase bonuses reward adjacent terms.

The ranking is deliberately understandable rather than mathematically perfect.
That is a sensible coursework decision because the video must show complete
understanding.

## Query Improvements

The search layer also supports:

- stop-word filtering for unquoted queries,
- conservative stemming, such as matching `friend` with `friends`,
- spelling suggestions when no result is found,
- snippets that show part of the matched document text.

These are useful higher-band features because they are built from the index
rather than bolted on as unrelated extras.

## Pros and Cons of Different Approaches

### AND Search

Pros:

- Precise results.
- Demonstrates posting-list intersection.
- Matches the expected behaviour for multi-word search.

Cons:

- Can return no results if the query is too specific.
- Requires query suggestions or clear messages for a better user experience.

### OR Search

Pros:

- More forgiving.
- Often returns something for broad queries.

Cons:

- Less precise.
- Can bury strongly relevant pages among weak matches.
- Easier to implement but less convincing as a search engine explanation.

### Exact Phrase Matching with Positions

Pros:

- Efficient once the index exists.
- Does not need to rescan full page text.
- Shows why positional statistics matter.

Cons:

- Requires a larger index.
- Needs careful handling of token order and punctuation.

### Text Rescanning for Phrases

Pros:

- Simpler if the original page text is stored.
- Avoids storing positions.

Cons:

- Slower for many queries.
- Can disagree with tokenised search if punctuation or case is handled
  differently.

### Simple Frequency Ranking

Pros:

- Easy to calculate and explain.
- Good enough for a small site.

Cons:

- Common words can dominate.
- Does not reward rare, more meaningful query terms.

### TF-IDF-Inspired Ranking

Pros:

- Rewards more informative words.
- Still explainable in a short video.
- Produces better ordering than frequency alone.

Cons:

- More complex than raw counts.
- Scores are relative and need explanation.
