# GenAI Usage Declaration and Critical Evaluation

This coursework was developed with assistance from OpenAI Codex/ChatGPT.

## What GenAI Helped With

- Interpreting the marking criteria and turning the brief into a concrete
  implementation checklist.
- Suggesting a clean module split: crawler, indexer, search, and command shell.
- Drafting tests that mock network access so the suite does not depend on the
  live website.
- Identifying edge cases worth testing, including empty queries, missing words,
  re-indexing the same URL, and politeness timing.
- Highlighting higher-band improvements such as exact phrase search, query
  suggestions, stemming, stop-word handling, benchmarking, and CI evidence.

## What Needed Human Review

- The crawler design had to be checked carefully against the coursework rule
  that there must be at least 6 seconds between requests.
- The index format needed to stay explainable for a 5-minute demonstration, so
  overly complex AI suggestions would have been inappropriate.
- Ranking is deliberately simple. TF-IDF plus a phrase bonus improves result
  ordering without hiding the core inverted-index behaviour.
- Generated code still needed manual inspection for maintainability, imports,
  error handling, and whether each part could be explained in the video.
- AI suggestions for "advanced search" can become too broad. I kept the final
  additions focused on features that directly use the inverted index: exact
  phrase checks from stored positions, vocabulary-based suggestions, conservative
  stemming, and unquoted stop-word filtering.

## Impact on Learning

GenAI accelerated scaffolding and helped produce a broader test suite, but it
did not remove the need to understand the algorithms. The most useful learning
came from checking each suggestion against the brief: what the posting lists
store, why positions matter, how multi-word queries are resolved, and how
politeness is enforced.

## Limitations and Ethical Considerations

AI can produce plausible code that does not fully satisfy the assessment. For
example, a crawler can appear correct while forgetting the 6 second delay, or a
search function can return pages matching any query word rather than every word.
All AI-assisted work must therefore be declared, reviewed, tested, and explained
honestly.
