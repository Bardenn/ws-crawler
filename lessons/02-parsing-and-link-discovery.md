# Lesson 2: Parsing and Link Discovery

## What This Component Does

After the crawler receives HTML, it must turn that page into useful data for the
rest of the search tool. Parsing has two jobs:

- extract text that should be searchable,
- discover links to other internal pages.

The implementation uses Beautiful Soup, which is appropriate for the coursework
brief and easier to explain than lower-level HTML parsing.

## Current Design

`parse_page` creates a Beautiful Soup object from the response HTML. It removes
non-content tags such as `script`, `style`, and `noscript`, because those tags
can contain text that users would not expect to search.

It then extracts:

- the page title from the `<title>` tag,
- the visible page text using `get_text`,
- links from `<a href="...">` elements.

Each link is converted into an absolute URL using the current page URL as the
base. The URL is then normalised so repeated versions of the same page are less
likely to appear as separate documents.

## Link Filtering

The crawler keeps only internal HTML-like URLs. It rejects:

- non-HTTP schemes,
- links to other domains,
- login and logout pages,
- static assets such as images, CSS, and JavaScript.

This is important because a search index should contain pages, not every file a
website links to.

## URL Normalisation

Normalisation removes fragments and query strings, ensures directory-style URLs
end with `/`, and treats `/page/1/` as the same page as `/`. This prevents
duplicate documents caused by small URL variations.

This is another useful GenAI reflection point. AI often suggests simply appending
every `href` to the queue. That works for a toy page but can duplicate URLs,
follow external links, or crawl irrelevant files. The improvement is to add
explicit filtering and normalisation rules.

## Teaching Example

Use one quote page as the example:

1. HTML arrives from the crawler.
2. Beautiful Soup removes non-visible content.
3. The remaining text becomes input for the indexer.
4. Anchor tags become candidate URLs.
5. URL checks decide what is safe to queue next.

## Pros and Cons of Different Approaches

### Beautiful Soup Parsing

Pros:

- Clear, readable API.
- Handles imperfect HTML well.
- Matches the coursework recommended libraries.

Cons:

- Slower than some lower-level parsers.
- Text extraction can include navigation text unless filtered further.

### Regular Expressions for HTML

Pros:

- Can be quick for tiny, known snippets.
- No extra parser concepts to learn.

Cons:

- Fragile with real HTML.
- Hard to handle nested tags, attributes, and malformed markup.
- Poor choice for a robust crawler.

### Indexing Full Page Text

Pros:

- Simple.
- Captures all visible words.
- Easy to explain and test.

Cons:

- May include repeated navigation text.
- Less precise than extracting only quotes, authors, and tags.

### Indexing Only Quote Content

Pros:

- More focused results.
- Less noise from menus and pagination.

Cons:

- More site-specific.
- Less like a general search engine crawler.
- More fragile if the page structure changes.
