# COMP3011 Coursework 2 Brief 2025/2026

**School:** School of Computer Science  
**Module title:** Web Services and Web Data  
**Module code:** COMP3011  
**Assignment title:** Coursework 2: Search Engine Tool  
**Assignment type:** Individual practical project with video demonstration  
**Weighting:** 30% of overall module mark  
**Submission deadline:** 8 May 2026  
**Submission method:** Electronic submission via Minerva: video demonstration link, GitHub repository URL, and index file  
**Feedback provision:** Electronic via Minerva  
**Module lead:** Dr Ammar Alsalka - M.A.Alsalka@leeds.ac.uk  
**Other staff contact:** Mr Omar Choudhry - O.Choudhry@leeds.ac.uk

---

## Rationale

This coursework helps develop skills in building web crawlers, indexers, and web search algorithms. It assesses your ability to:

- Understand how search engines work.
- Write efficient code for web crawling, indexing, and query processing.
- Learn techniques for storing words in search indices.
- Implement algorithms for ranking and retrieving search terms from indices.

---

## Word Limit and Guidance

The primary assessment component is a **5-minute video demonstration**, accompanied by:

- A GitHub repository.
- An index file submission.

---

## Use of GenAI in This Assessment

This assessment is categorised as **GREEN**.

AI has an integral role and should be used as part of the assessment. You may use GenAI as a primary tool throughout the assessment process.

A core part of this assessment, worth **15% of the grade**, is your critical reflection on GenAI usage in your video demonstration. You must discuss:

- Specific examples of where GenAI helped or hindered your work.
- The quality of AI-generated code.
- How using, or not using, GenAI affected your learning.

Non-declared or misleading declaration of GenAI use constitutes academic misconduct.

---

## Learning Outcomes Assessed

- Understanding of search engine mechanisms.
- Efficient coding for web crawling, indexing, and query processing.
- Knowledge of search index storage techniques.
- Implementation of ranking and retrieval algorithms.
- Critical evaluation of Generative AI tools.
- Comprehensive testing and version control practices.

---

# 1. Assignment Guidance

You will develop a search tool that can:

1. Crawl the pages of a website.
2. Create an inverted index of all word occurrences in the pages of the website.
3. Allow the user to find pages containing certain search terms.

Your work will be assessed through a **5-minute video demonstration** that showcases your implementation, explains your design decisions, demonstrates testing, and provides a critical evaluation of any GenAI tools used.

---

## 1.1 Target Website

The website for this project is:

```text
https://quotes.toscrape.com/
```

This website contains a collection of common quotes and is purpose-built to help people learn web scraping.

---

## 1.2 Important Requirements

### Politeness Window

You must observe a politeness window of at least **6 seconds** between successive requests to the website.

### Inverted Index

The tool must create an inverted index as it crawls the website. The index must store statistics for each word in each page, such as:

- Frequency.
- Position.
- Other useful occurrence statistics.

### Case Sensitivity

For simplicity, search is **not case sensitive**.

For example:

```text
Good == good
```

---

## 1.3 Technical Requirements

You should use **Python** to implement the search tool.

Recommended libraries:

- [Requests](http://docs.python-requests.org/en/master/) for composing HTTP requests.
- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) for parsing HTML pages.

---

## 1.4 Command-Line Interface

The search tool must have a command-line interface, or shell, and provide the following commands.

### `build`

The `build` command crawls the website, builds the index, and saves the resulting index into the file system.

For simplicity, the entire index can be saved to a single file.

Example:

```shell
> build
```

### `load`

The `load` command loads the index from the file system.

This command only works if the index has previously been created using the `build` command.

Example:

```shell
> load
```

### `print`

The `print` command prints the inverted index for a particular word.

Example:

```shell
> print nonsense
```

This prints the inverted index for the word `nonsense`.

### `find`

The `find` command finds a given query phrase in the inverted index and returns a list of all pages that contain it.

Examples:

```shell
> find indifference
> find good friends
```

The first example returns all pages containing the word `indifference`.

The second example returns all pages containing the words `good` and `friends`.

---

# 2. Use of GenAI

This assessment is **Green Category**. AI tools may be used with proper declaration and critical evaluation.

You are permitted to use GenAI under the following conditions.

---

## 2.1 Declaration

You must clearly state which AI tools you used and for what purposes in your video demonstration.

---

## 2.2 Critical Evaluation

A core part of this assessment, worth **15% of the grade**, is your critical reflection on GenAI usage.

In your video, you must:

- Discuss specific examples of where GenAI helped or hindered your work.
- Analyse the quality and correctness of AI-generated code or suggestions.
- Reflect on how using, or not using, GenAI affected your learning.
- Discuss any challenges in understanding or debugging AI-generated code.
- Evaluate the impact on your development process and time management.

---

## 2.3 Understanding

You must demonstrate complete understanding of all code in your submission, whether AI-assisted or not.

You should be able to:

- Explain every line of code.
- Justify all design decisions.

---

## 2.4 If You Do Not Use GenAI

If you choose not to use GenAI tools, you must discuss this decision in your video and reflect on your development experience without AI assistance.

---

## 2.5 Example GenAI Evaluation Topics

Good critical evaluations might discuss:

- AI suggested an incorrect data structure for the inverted index, which you debugged and improved.
- AI helped you understand BeautifulSoup's API, but you had to modify its example code significantly.
- You chose not to use AI for core algorithms to ensure you truly understood the implementation.
- AI-generated tests missed several edge cases that you had to identify and add manually.

---

## 2.6 Academic Misconduct Warning

Non-declaration or misleading declaration of GenAI use constitutes academic misconduct.

To ensure privacy and data security, use only the University's secure Copilot access when engaging with AI tools.

---

# 3. Assessment Tasks

You must write code and create a **5-minute video demonstration** presenting your design and implementation.

---

## 3.1 Video Demonstration Requirements

The 5-minute video demonstration is the primary assessment component.

The video must be uploaded to an accessible platform, such as:

- Google Drive.
- YouTube.
- OneDrive.
- Similar platform.

The link must be submitted via Minerva.

Before submitting, check that the link works by opening it in an incognito or private browser window.

---

## 3.2 What to Include in the Video

### A. Live Demonstration - 2 minutes

Show your search tool running all four commands:

- `build`
- `load`
- `print`
- `find`

Also demonstrate:

- Handling of multi-word queries.
- Edge cases, such as:
  - Non-existent words.
  - Empty queries.

### B. Code Walkthrough and Design Decisions - 1.5 minutes

Explain:

- Your choice of data structures for the inverted index.
- Key sections of your code:
  - Crawler.
  - Indexer.
  - Search logic.
- Your implementation choices.
- Any trade-offs made.

### C. Testing Demonstration - 0.5 minutes

Show your test suite running.

Explain:

- Your testing strategy.
- Your test coverage.

### D. Version Control - 0.5 minutes

Show your Git commit history demonstrating regular, incremental development.

Briefly explain your development workflow.

### E. GenAI Critical Evaluation - 0.5 minutes

Critically evaluate any GenAI tools used, if applicable.

Discuss:

- Specific examples of where GenAI helped or hindered your work.
- Your learning experience with or without GenAI.

---

## 3.3 Video Technical Requirements

- **Duration:** Maximum 5 minutes. Videos exceeding 5 minutes will have marks deducted.
- **Format:** MP4, MOV, or similar standard video format.
- **Resolution:** 720p minimum.
- **Hosting:** Google Drive, YouTube, OneDrive, or similar platform.
  - YouTube videos should be unlisted, not private.
  - OneDrive links should be shared with "Anyone at the University of Leeds".
- **Accessibility:** Ensure the video link is accessible to markers by checking sharing permissions.
- **Audio and visual quality:** Clear audio narration and legible screen recording.
- **Screen recording:** Use appropriate screen recording software to show your code and terminal.

---

## 3.4 GitHub Repository Structure

Your GitHub repository should be organised as follows:

```text
repository-name/
├── src/
│   ├── crawler.py
│   ├── indexer.py
│   ├── search.py
│   └── main.py
├── tests/
│   ├── test_crawler.py
│   ├── test_indexer.py
│   └── test_search.py
├── data/
│   └── [compiled index file]
├── requirements.txt
└── README.md
```

---

## 3.5 README Requirements

Your `README.md` must include:

- Project overview and purpose.
- Installation and setup instructions.
- Usage examples for all four commands.
- Testing instructions.
- Dependencies and how to install them.

---

# 4. General Guidance and Study Support

Detailed information and guidance on building search tools are available in the module's learning resources on Minerva.

---

## 4.1 Recommended Resources

- Module lecture slides on web crawling, indexing, and search algorithms.
- Python Requests library documentation: <http://docs.python-requests.org/en/master/>
- Beautiful Soup documentation: <https://www.crummy.com/software/BeautifulSoup/bs4/doc/>
- Target website for practice: <https://quotes.toscrape.com/>

---

## 4.2 Getting Help

If you encounter difficulties or have questions about the assignment:

- Attend module practical lab sessions where teaching staff can provide guidance.
- Post questions on the module discussion forum on Minerva.
- Contact the module leader or teaching staff during office hours.

---

## 4.3 Key Implementation Tips

- **Test incrementally:** Build and test each component, such as crawler, indexer, and search, separately before integration.
- **Write tests as you go:** Do not leave testing until the end. Build your test suite alongside your implementation.
- **Commit regularly:** Make frequent Git commits with meaningful messages to demonstrate your development process.
- **Handle errors gracefully:** Network requests can fail, so implement appropriate error handling.
- **Document your code:** Clear comments and docstrings will help when creating your video explanation.
- **Respect the politeness window:** Always wait at least 6 seconds between requests.
- **Choose appropriate data structures:** Consider efficiency for both indexing and searching operations.
- **Plan your video:** Script or outline your video before recording to ensure you cover all required components within 5 minutes.
- **Practice your demonstration:** Do a dry run to check timing and ensure everything works smoothly.

---

## 4.4 Video Recording Tips

- Use screen recording software like OBS Studio, which is free, or QuickTime on Mac.
- You may prepare recorded videos in a PowerPoint presentation and record the video using Microsoft PowerPoint itself.
- Test your audio levels before recording the full video.
- Use a quiet environment with minimal background noise.
- Consider using a script or bullet points to stay on track.
- If you make a mistake, you can edit the video or re-record.
- Zoom in on code and terminal output so text is clearly readable.
- Consider adding captions or text overlays for key points.

---

# 5. Assessment Criteria and Marking Process

## 5.1 Assessment Criteria

| Criterion | Weighting | Requirements |
|---|---:|---|
| Crawling Implementation | 10% | Successfully crawls all pages, respects politeness window, handles errors. |
| Indexing Implementation | 10% | Creates correct inverted index with word statistics. |
| Storage and Retrieval | 8% | Correctly implements `build` and `load`; saves and loads index from file system. |
| Search Functionality | 12% | Correctly implements `print` and `find` for single-word and multi-word queries. |
| Testing and Test Coverage | 20% | Comprehensive test suite covering edge cases, documented testing strategy. |
| Code Quality and Documentation | 10% | Clear code structure, appropriate data structures, inline comments, README. |
| Version Control and Git Practices | 5% | Regular commits with meaningful messages, demonstrates incremental development. |
| Video Demonstration Quality | 10% | Clear presentation, well-structured, covers all required components, good timing. |
| GenAI Critical Evaluation | 15% | Thoughtful reflection, specific examples, learning insights. |
| **Total** | **100%** |  |

---

## 5.2 Grading Bands

### 40-49 - Pass

Expected features:

- Basic working implementation of all four commands.
- Crawls most pages but may miss some or have minor errors.
- Inverted index created with a basic structure.
- Some tests present but limited coverage, less than 50%.
- Git history shows development, but commits may be irregular or poorly described.
- Video demonstrates basic functionality but lacks a clear explanation.
- GenAI evaluation is present but superficial, such as simply saying "I used ChatGPT and it was helpful".
- Code has minimal documentation and some structural issues.

### 50-59 - Satisfactory

Expected features:

- All four commands work correctly on standard inputs.
- Crawler successfully retrieves all pages and respects the politeness window.
- Inverted index correctly stores word statistics.
- Test suite has reasonable coverage, between 50% and 70%, and covers main functionality.
- Regular Git commits with descriptive messages.
- Video clearly demonstrates all functionality with adequate explanations.
- GenAI evaluation discusses specific uses, such as using GenAI for debugging a particular issue.
- Code is readable with some documentation.
- Basic README is present.
- Some basic error handling is implemented.

### 60-69 - Good

Expected features:

- Robust implementation handling edge cases, such as empty queries and special characters.
- Efficient crawler with proper error handling for network issues.
- Well-designed inverted index with appropriate data structures.
- Comprehensive test suite with 70% to 85% coverage, including edge cases.
- Consistent Git workflow with meaningful commit messages, showing iterative development.
- Video is well-structured and clearly explains design decisions and trade-offs.
- GenAI evaluation is thoughtful and discusses both benefits and limitations with examples.
- Clean, well-documented code with clear structure and inline comments.
- Good README with setup instructions and usage examples.

### 70-79 - Very Good

Expected features:

- Excellent implementation with optimised data structures and algorithms.
- Crawler efficiently handles various HTML structures and error conditions.
- Sophisticated inverted index design with justification for choices.
- Extensive test suite with more than 85% coverage, including unit, integration, and performance tests.
- Exemplary Git practices, such as feature branches, clear commit history, and logical progression.
- Professional video presentation with clear narrative, good pacing, and visual aids.
- Insightful GenAI evaluation critically analysing the impact on learning and the development process.
- High-quality code following Python best practices, including PEP 8 and modular design.
- Comprehensive README with architecture overview and design rationale.
- Code includes defensive programming and graceful error recovery.

### 80-100 - Excellent to Outstanding

Expected features:

- Exceptional implementation demonstrating deep understanding and innovation.
- Advanced features beyond requirements, such as:
  - TF-IDF ranking.
  - Advanced query processing.
  - Query suggestions.
- Highly optimised algorithms with complexity analysis and benchmarking.
- Professional-grade test suite with extensive coverage, mocking, and automated testing pipeline.
- Professional Git workflow with semantic commits, tags or releases, and branching strategy.
- Outstanding video that is engaging, demonstrates mastery, and discusses algorithmic trade-offs.
- Sophisticated GenAI evaluation showing critical thinking about AI's role in software development, including ethical considerations or learning implications.
- Publication-quality code with exemplary structure, comprehensive documentation, type hints, and docstrings.
- Professional README comparable to open-source projects.
- Evidence of research into search engine algorithms and modern practices.
- For 90-100: novel contributions or particularly creative solutions to challenges.

---

# 6. Presentation and Referencing

The quality of communication in your video and code documentation will be assessed.

As a minimum, you must ensure:

- Your explanation follows a logical structure.
- You reference any external resources, libraries, or tutorials used.
- Your narration clearly communicates your implementation approach.
- Technical terminology is used appropriately.

---

# 7. Submission Requirements

## 7.1 What to Submit via Minerva

You must submit a single text document, either **PDF** or **TXT**, via Minerva containing the following.

### A. Video Demonstration Link

Submit the URL to your 5-minute video.

Acceptable platforms include:

- Google Drive.
- YouTube.
- OneDrive.
- Similar platform.

Requirements:

- Ensure sharing permissions are set correctly and the video is accessible to anyone with the link.
- Test the link in an incognito or private browser window before submission.

### B. GitHub Repository URL

Submit a link to your public GitHub repository containing:

- All source code files.
- Comprehensive `README.md` with setup and usage instructions.
- Test files and testing documentation.
- Any auxiliary files needed to run the tool.

### C. Index File

Attach the compiled index file generated by your search tool.

This can be:

- Uploaded as a separate attachment on Minerva.
- Included as a download link if the file is too large.

---

## 7.2 Late Submissions

Late submissions without approved mitigation will be penalised according to University of Leeds guidelines:

- Late submissions without approved mitigation incur a **5% penalty per day**.
- Maximum extension period for mitigating circumstances is **2 weeks**.

---

# 8. Academic Misconduct and Plagiarism

Leeds students are part of an academic community that shares ideas and develops new ones.

You need to learn how to:

- Work with others.
- Interpret and present other people's ideas.
- Produce your own independent academic work.
- Distinguish between other people's work and your own.
- Correctly acknowledge others' work.

All students new to the University are expected to complete an online Academic Integrity tutorial and test. All Leeds students should ensure that they are aware of the principles of Academic Integrity.

When you submit work for assessment, it is expected that it meets the University's academic integrity standards.

If you do not understand these standards, or how they apply to your work, ask the module teaching staff for further guidance.

By submitting this assignment, you confirm that:

- The work is a true expression of your own work and understanding.
- You have declared all GenAI tools used, or stated that none were used.
- You can explain and justify all code and design decisions in your submission.
- You have given credit to others, including AI tools, where their work has contributed to yours.

---

# Quick Checklist

## Implementation

- [ ] Python search tool created.
- [ ] Crawler implemented.
- [ ] Politeness window of at least 6 seconds between requests.
- [ ] Inverted index created.
- [ ] Word statistics stored, such as frequency and position.
- [ ] Search is case-insensitive.
- [ ] `build` command works.
- [ ] `load` command works.
- [ ] `print` command works.
- [ ] `find` command works.
- [ ] Multi-word queries handled.
- [ ] Edge cases handled, such as empty queries and non-existent words.

## Testing

- [ ] Unit tests for crawler.
- [ ] Unit tests for indexer.
- [ ] Unit tests for search.
- [ ] Edge cases tested.
- [ ] Test suite can be shown running in the video.
- [ ] Testing strategy documented.

## Repository

- [ ] Repository follows required structure.
- [ ] `src/` folder included.
- [ ] `tests/` folder included.
- [ ] `data/` folder includes compiled index file.
- [ ] `requirements.txt` included.
- [ ] `README.md` included.
- [ ] Git commit history shows regular incremental development.

## README

- [ ] Project overview included.
- [ ] Installation/setup instructions included.
- [ ] Usage examples for `build`, `load`, `print`, and `find` included.
- [ ] Testing instructions included.
- [ ] Dependencies listed.

## Video

- [ ] Maximum 5 minutes.
- [ ] 720p minimum resolution.
- [ ] Clear audio narration.
- [ ] Code and terminal text are readable.
- [ ] Shows live demo of `build`, `load`, `print`, and `find`.
- [ ] Shows multi-word queries.
- [ ] Shows edge cases.
- [ ] Explains data structures and design decisions.
- [ ] Shows test suite running.
- [ ] Shows Git commit history.
- [ ] Includes GenAI critical evaluation.
- [ ] Link permissions tested in incognito/private browser.

## Submission

- [ ] Single text document submitted via Minerva containing video link and GitHub URL.
- [ ] Video demonstration link included.
- [ ] GitHub repository URL included.
- [ ] Compiled index file attached or linked.
- [ ] GenAI use declared, or no GenAI use stated.
