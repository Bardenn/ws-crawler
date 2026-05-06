# Lesson 1: Polite Crawling

## What This Component Does

The crawler is responsible for visiting pages on `https://quotes.toscrape.com/`
and returning structured page objects containing:

- the page URL,
- the page title,
- the searchable text,
- internal links discovered on that page.

The most important coursework rule is the politeness window: the tool must wait
at least 6 seconds between successive requests to the target site.

## Current Design

The crawler is represented by `QuoteCrawler`. It stores the base URL, maximum
page count, timeout, HTTP session, and timing functions. The crawler uses an HTTP
session so headers such as the user agent are applied consistently.

The crawling loop keeps three collections:

- `queue`: URLs waiting to be visited.
- `queued`: URLs already scheduled, to avoid duplicate work.
- `visited`: URLs already fetched or attempted.

The crawler fetches URLs until either the queue is empty or the `max_pages` limit
is reached. Each successful response is parsed into a `CrawledPage`, then its
internal links are added to the queue.

## Politeness Logic

Before each request, `_wait_if_needed` compares the current monotonic time with
the timestamp of the previous request. If fewer than `politeness_delay` seconds
have passed, it sleeps for the remaining time.

The first request does not sleep, because there has not yet been a previous
request. After every request, the crawler updates `_last_request_time`.

This is a good example to discuss critical GenAI use: an AI-generated crawler may
look correct while forgetting the timing rule, or it may sleep after parsing
rather than before the next request. The human check is to trace the request
sequence and verify that every pair of network calls is separated by at least 6
seconds.

## Why Dependency Injection Helps

The crawler accepts `sleep_fn`, `monotonic_fn`, and an optional HTTP session.
This makes the crawler testable without real network delays:

- fake sessions return controlled HTML,
- fake clocks simulate elapsed time,
- fake sleep functions record the requested delay.

That is better than waiting 6 real seconds inside unit tests.

## Teaching Example

In the video, explain the crawler as a controlled queue:

1. Start with the homepage.
2. Fetch one page politely.
3. Parse its useful text and links.
4. Add only valid internal links.
5. Repeat until the page limit is reached.

## Pros and Cons of Different Approaches

### Breadth-First Crawling

Pros:

- Easy to explain.
- Finds nearby site pages before deep pages.
- Works well for the small coursework website.

Cons:

- Can grow a large queue on bigger websites.
- Does not prioritise pages by content relevance.

### Depth-First Crawling

Pros:

- Simple recursive idea.
- Uses less queue memory in small cases.

Cons:

- Can go deep into one path and miss more representative pages.
- More awkward to combine with page limits and duplicate prevention.

### Synchronous Requests

Pros:

- Simple and transparent.
- Easier to satisfy and explain the 6 second delay.
- Easier to test deterministically.

Cons:

- Slow for large crawls.
- Does not use network waiting time efficiently.

### Asynchronous Requests

Pros:

- Much faster for large multi-domain crawling.
- Can keep many requests in progress.

Cons:

- More complex.
- Riskier for this coursework because politeness must be enforced carefully.
- Harder to explain in a 5-minute video.
