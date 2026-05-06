# Lesson 6: Critical GenAI Usage

## Why This Matters

The brief says this is a Green Category assessment, so GenAI can be used as a
primary tool. It also says 15% of the grade is for critical reflection. That
means the video should not simply say "I used AI." It should show judgement:
where AI helped, where it was risky, and how the final work was checked.

## Specific Helpful Uses

GenAI was useful for turning the brief into an implementation plan:

- separate modules for crawling, indexing, searching, and the shell,
- an inverted index structure with frequencies and positions,
- mocked tests so the crawler could be tested without live requests,
- extra search features such as exact phrases, stop-word handling, suggestions,
  and TF-IDF-style ranking,
- documentation and video structure.

These are good examples because they are concrete and tied to visible code.

## Specific Risks and Corrections

The strongest critical points are the places where AI suggestions needed human
checking:

- A crawler can miss the 6 second politeness rule even if it otherwise works.
- A multi-word search can accidentally use OR semantics instead of requiring all
  query words.
- An index can store frequencies but forget positions, making phrase search
  harder.
- Re-indexing the same URL can duplicate postings unless old entries are
  removed first.
- Tests can be generated around existing behaviour rather than the brief's
  actual requirements.

These points show that GenAI did not replace understanding. It accelerated
drafting, but the final design still had to be reasoned about.

## Quality of AI-Generated Code

The useful parts of AI-generated code were usually structural:

- suggesting classes and function boundaries,
- proposing edge cases,
- drafting repetitive test scaffolding,
- explaining library APIs.

The weaker parts were areas with hidden requirements:

- timing and politeness,
- exact query semantics,
- maintainable index format,
- keeping features explainable in a 5-minute video.

This distinction is important. AI can write plausible code quickly, but
plausible code is not automatically correct code.

## Effect on Learning

Using GenAI helped learning when it was treated like a tutor or reviewer. It
gave quick explanations of concepts such as inverted indexes, posting lists,
TF-IDF, and mocking.

It would have harmed learning if the code had been accepted without tracing it.
The useful learning came from asking:

- What data is stored for each word?
- Why do positions matter?
- How does posting-list intersection work?
- Where is the 6 second delay enforced?
- What does each test prove?

## Suggested Video Script

"I used OpenAI Codex/ChatGPT during the project. It was most helpful for
planning the module split and identifying tests, especially mocked crawler tests
so I did not have to wait 6 seconds in every unit test. However, I did not just
accept generated code. I checked it against the brief. For example, the crawler
has to wait at least 6 seconds between requests, and multi-word search has to
return pages containing every query term. Those are places where a plausible AI
answer could still be wrong. I also kept the index format explainable: it stores
frequency and positions, which lets me demonstrate both `print` and exact phrase
search."

## Pros and Cons of Different GenAI Approaches

### Using GenAI for Planning

Pros:

- Quickly turns requirements into a checklist.
- Helps identify missing components.
- Good for comparing design options.

Cons:

- Can over-scope the project.
- May suggest features that are impressive but hard to explain.

### Using GenAI for Code Drafting

Pros:

- Speeds up boilerplate.
- Helps with unfamiliar APIs.
- Can produce a working first version quickly.

Cons:

- May hide bugs behind confident-looking code.
- Can introduce abstractions that are unnecessary for the brief.
- Requires careful review to ensure you can explain every line.

### Using GenAI for Testing Ideas

Pros:

- Good at listing edge cases.
- Helps create mocked tests for network code.
- Encourages broader coverage.

Cons:

- Tests may reflect the implementation rather than the requirement.
- Generated tests may miss timing, ordering, or persistence edge cases.

### Using GenAI for Explanation

Pros:

- Helps turn code into teaching language.
- Useful for preparing the video.
- Can clarify trade-offs between approaches.

Cons:

- Explanations can sound generic unless tied to exact code decisions.
- The speaker still needs genuine understanding for questions and assessment.
