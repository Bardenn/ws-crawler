# Lesson 5: Command Shell, Persistence, and Testing

## What This Component Does

The command-line shell turns the crawler, indexer, and search engine into a tool
that can be demonstrated. The required commands are:

- `build`
- `load`
- `print`
- `find`

The shell also provides helpful messages for missing indexes, empty queries, and
unknown words.

## Current Design

`SearchShell` stores the index path, base URL, politeness delay, maximum page
count, current index, and current search engine.

The command flow is:

- `build`: crawl pages, build an index, save JSON, and keep it loaded.
- `load`: read a saved JSON index from disk.
- `print WORD`: display the posting list for one word.
- `find QUERY`: run the search engine and print ranked results.

There is also a non-interactive `--command` option, which is useful for tests and
for quick video demonstrations.

## Persistence

The index is stored in `data/index.json`. JSON is not the most compact format,
but it is readable and easy to submit. It also makes the data structure visible
in the video: metadata, documents, terms, URLs, frequencies, and positions can
all be inspected directly.

## Testing Strategy

The test suite checks each component separately:

- crawler tests use fake HTTP sessions,
- politeness tests use fake time and fake sleep,
- indexer tests check tokenisation, frequencies, positions, replacement, and
  JSON save/load,
- search tests check lookup, AND queries, phrases, stemming, stop words,
  suggestions, and ranking,
- CLI tests check user-facing command output,
- end-to-end tests run the module as a subprocess.

This testing setup is strong evidence for the video because it shows that the
tool was not only generated and trusted. It was checked against the brief.

## GenAI Reflection Point

GenAI is helpful for suggesting edge cases, especially cases a student might not
think of immediately:

- empty query input,
- missing index file,
- repeated page indexing,
- typo suggestions,
- case-insensitive searches,
- fake network tests.

The limitation is that generated tests can confirm the implementation's current
behaviour rather than the coursework requirement. Human review is needed to ask:
"Is this the correct behaviour, or just behaviour the code already has?"

## Pros and Cons of Different Approaches

### Interactive Shell

Pros:

- Matches the coursework command examples.
- Easy to demonstrate live.
- Lets the marker try multiple queries quickly.

Cons:

- Requires careful input parsing.
- More stateful than one-off commands because the index can be loaded or not
  loaded.

### One-Off Command-Line Arguments

Pros:

- Easier to automate.
- Good for tests and scripts.

Cons:

- Less like the required shell examples.
- Can be clumsier for a live demonstration.

### JSON Persistence

Pros:

- Human-readable.
- Easy to submit.
- Easy to load with Python's standard library.

Cons:

- Larger than binary formats.
- Slower than a database for large indexes.

### Database Persistence

Pros:

- Scales better.
- Supports incremental updates and more complex queries.

Cons:

- More setup.
- Harder to inspect in a short video.
- Unnecessary for the small target website.

### Mocked Unit Tests

Pros:

- Fast and deterministic.
- Avoid real network delays.
- Can test failure cases reliably.

Cons:

- May miss behaviour of the live website.
- Need realistic fixtures to be meaningful.

### Live End-to-End Tests

Pros:

- Prove the real website can be crawled.
- Catch integration issues.

Cons:

- Slow because of the 6 second politeness rule.
- Can fail because of network or website availability rather than code defects.
