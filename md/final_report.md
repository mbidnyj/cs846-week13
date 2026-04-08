# App Coding Comparison Report
**CS 846: LLMs for Software Engineering (Winter 2026)**

- **Student Name:** *Maksym Bidnyi*
- **Student ID:** *21226476*
- **Date Submitted:** April 7, 2026
- **AI Tools Used in This Report:** Claude Code (structuring and polishing the draft)

---

## 1. App Description

The assigned application is a microblogging web app (Twitter-like proof of concept). Users can register an account, log in, create short text posts, browse a global chronological feed with pagination, like other users' posts, reply to posts (one level deep), and view public user profiles. The app is constrained to a single global feed (no follower graph), no private messaging, and no reposts. All data is stored in-memory with no persistent database. The stack is intentionally minimal: a Python backend exposing a REST API with a lightweight frontend consuming it. Both the Week 2 and Week 13 versions implement the same specification; they differ in the development process and the guidelines applied while building them.

---

## 2. Guidelines Applied and Not Applied

### 2.1 Guidelines Applied

| Guideline | Source (Week / Paper / Blog) | Where / How I Applied It | Observed Effect |
|-----------|------------------------------|--------------------------|-----------------|
| Design a structured context prompt | Week 4, Requirements Engineering (Guideline 1) | Before coding, I wrote a structured requirements document covering features, constraints, and technical decisions, plus a longer phased implementation spec with endpoint contracts, request/response formats, and validation rules. These served as the "job description" for the LLM. | The LLM produced endpoints that matched the spec on the first pass. Fewer corrections compared to Week 2, where I was making things up as I went. |
| Treat LLM output as a draft, not a final product | Week 4, Requirements Engineering (Guideline 14) | I reviewed every generated endpoint for correctness before moving on. Found and corrected issues like missing error handling for edge cases (e.g., liking your own post, duplicate likes). | Caught subtle logic bugs early. In Week 2, I accepted Copilot output more readily and hit issues later (e.g., a missing import error that took multiple iterations to resolve). |
| Focus on higher-level functionality, not implementation | Week 5, Code Summarization (Guideline 4) | In the implementation spec, I described each endpoint by its contract (what it accepts, what it returns, what validations apply) rather than prescribing how to code it. | The LLM had freedom to choose clean patterns (dataclasses, reusable helpers) rather than being locked into a specific approach. |
| Specify project-specific tool and workflow execution mechanics | Week 6, Code Generation (Guideline 1) | Created a project instruction file at the repository root with exact commands for activating the environment, installing dependencies, starting the server, and running tests. | The LLM could run tests and verify changes without guessing the setup. In Week 2, framework-specific commands (migrations, redirect settings) were a recurring friction point. |
| Work in short, iterative cycles | Week 6, Code Generation (Guideline 5) | Broke implementation into 3 phases: (1) User & Session Management, (2) Posting System, (3) Likes, Replies, Feed. Each phase had its own checklist. | Each module was testable before building the next layer. Issues stayed local to one phase instead of cascading. |
| Control prompt details based on solution certainty | Week 8, DevReview / Debugging (Guideline 4) | For well-understood features (CRUD endpoints), I gave detailed specs. For the frontend SPA, I kept the prompt general ("build a tabbed single-page interface for these API endpoints") and let the LLM design the UI. | CRUD endpoints were generated correctly on the first try. The frontend came back with a reasonable tab-based layout I would not have specified myself. |
| Specify edge cases and important details | Week 8, DevReview / Debugging (Guideline 6) | In the implementation spec, I explicitly listed validations: "user is author" checks for edit/delete, "user has not already liked" for likes, "non-empty content" for posts, offset/limit bounds for pagination. | All edge cases were implemented in the generated code without additional prompting. In Week 2, edge cases like a login redirect to a non-existent page were missed entirely. |
| Create a structured instruction file | Week 10, Code Review (Guideline 9) | Created a repository-level instruction file with project overview, architecture description, key patterns (session auth via Authorization header), and run commands. | The LLM maintained consistent patterns across all endpoints (same auth helper, same error format, same JSON structure). |

### 2.2 Guidelines Not Applied (and Why)

| Guideline | Source (Week / Paper / Blog) | Reason Not Applied |
|-----------|------------------------------|--------------------|
| Explicitly restrict output to the standard logging library | Week 12, Logging (Guideline 1) | The app is a 3-hour POC with in-memory storage and no production deployment. Adding structured logging would have consumed time without meaningful benefit. |
| Ask the LLM to analyze complexity before optimizing | Week 11, Performance (Guideline 1) | All data structures are in-memory dicts and lists with at most a few dozen entries during local testing. There are no bottlenecks to analyze at this scale. |
| Use automated CI gates (static analysis + LLM review) | Week 10, Code Review (Guideline 10) | Setting up Semgrep, CodeQL, or any CI pipeline was out of scope for a single-session POC. The codebase is small enough that manual review sufficed. |

---

## 3. Evaluation Criteria

| # | Criterion | Description | Why It Matters |
|---|-----------|-------------|----------------|
| 1 | Upfront Planning Quality | How well-defined were the requirements and implementation plan before writing code? Includes structured specs, endpoint contracts, phased breakdowns, and technical decision documentation. | The course emphasizes that structured context prompts directly improve LLM output quality. This criterion tests whether that investment pays off. |
| 2 | Feature Completeness | Did the app implement all seven required features (registration, login, posting, feed with pagination, likes, replies, public profiles) within the 3-hour session? | Both apps had the same time budget. Completeness reflects how well the development process used that time and whether guidelines helped or hindered throughput. |
| 3 | Code Structure & Maintainability | Separation of concerns (models vs routes vs frontend), consistency of patterns across endpoints, use of helper functions, and readability for someone new to the codebase. | A well-structured codebase is easier to extend and debug. This reveals whether guidelines led to cleaner architecture or just more ceremony. |
| 4 | Error Handling & Edge Cases | Input validation, proper HTTP status codes, boundary condition checks (empty content, duplicate likes, self-likes, pagination bounds), and clear error messages. | Robust error handling is one of the first things to degrade under time pressure. The course guidelines explicitly recommend specifying edge cases, so this tests whether that made a measurable difference. |
| 5 | Development Friction | How many bugs, configuration errors, or rework cycles occurred during the session? Includes import errors, migration issues, redirect problems, and other obstacles that consumed time without advancing features. | Even if both apps reach the same end state, the path matters. Lower friction means more time for features and suggests the process was better suited to AI-assisted work. |

---

## 4. Comparison of the Two Apps

| Criterion | Week 2 App | Week 13 App | Justification |
|-----------|-----------|------------|---------------|
| Upfront Planning Quality | 2/5 | 5/5 | Week 2 had informal planning via Copilot chat but no standalone spec. Week 13 had a structured requirements document and a detailed phased implementation spec with endpoint contracts, validations, and checklists. |
| Feature Completeness | 5/5 | 5/5 | Both apps implement all seven required features. Both achieved full coverage within the 3-hour session. |
| Code Structure & Maintainability | 3/5 | 4/5 | Week 2 used Django's built-in structure (models, views, URLs, templates, migrations), which provides good separation but is heavier. Views mixed template rendering and API logic in one file. Week 13 has a minimal three-file backend with consistent patterns: every endpoint uses the same auth helper, the same error format, and the same JSON structure. |
| Error Handling & Edge Cases | 3/5 | 4/5 | Week 2 relies on Django's ORM constraints (unique likes, 280-char limit) but has gaps, e.g., unauthenticated users fall back to a hardcoded user instead of returning an error. Week 13 explicitly checks every edge case in the route handlers: duplicate likes, self-likes, empty content, pagination bounds, author-only edit/delete. |
| Development Friction | 2/5 | 4/5 | Week 2 hit multiple configuration issues: missing migrations, a missing import error (took several iterations), login redirect to a non-existent page, and a database constraint error. Week 13 had a smoother session because the spec and instruction file meant the LLM knew the setup and contracts upfront. One hard bug still required switching to Claude Code. |

---

## 5. What Worked

**The structured context prompt (Week 4, Guideline 1) was the single highest-impact guideline.** In Week 2, I started coding almost immediately. In Week 13, I spent roughly 20 to 30 minutes writing structured requirements and a phased implementation spec before generating any code. This front-loaded investment paid for itself several times over: the LLM produced endpoints that matched the spec on the first attempt, edge cases were already enumerated, and I rarely had to re-explain intent.

**The instruction file (Week 10, Guideline 9) eliminated environment friction.** A short repository-level file told the LLM exactly how to activate the environment, install dependencies, and run the server and tests. In Week 2, framework-specific commands (migrations, redirect settings) were a recurring source of errors because the LLM had to guess my setup.

**Specifying edge cases explicitly (Week 8, Guideline 6) produced noticeably better validation.** In the implementation spec, I wrote out every validation rule: "user is author" for edit/delete, "user has not already liked" for likes, pagination bounds. All of these appeared in the generated code without additional prompting. In Week 2, a hardcoded user fallback for unauthenticated requests shows what happens when edge cases are left implicit: the LLM invented a workaround instead of raising an error.

**Short iterative cycles (Week 6, Guideline 5) kept issues contained.** Building auth before posts before likes/replies/feed meant each phase could be tested independently. In Week 2, I followed a similar incremental approach intuitively, but without explicit phase boundaries, which led to moments where features were built on untested foundations.

---

## 6. What Did Not Work

**Some guidelines were irrelevant at this scale, and knowing which to skip was itself a skill.** The logging guidelines (Week 12) and performance guidelines (Week 11) are well-reasoned for production systems, but in a 3-hour POC with in-memory storage, applying them would have been pure overhead. I noted them in my guidelines summary but did not invest time implementing them. Time saved went toward completing all features.

**"Treat LLM output as a draft" (Week 4, Guideline 14) is correct in principle but hard to practice consistently under time pressure.** In a 3-hour session, there is a natural tension between reviewing carefully and shipping features. I reviewed most output, but I still accepted the frontend JavaScript largely as-is because it worked on first render. Whether I would have caught subtle issues with more review time is unclear.

**The planning documents had diminishing returns past a certain detail level.** The implementation spec grew longer than necessary, with duplicated sections (the pagination checklist appears twice) and an API documentation table that was never consumed by anyone. Writing specs is useful, but there is a point where more detail does not produce better code. In a third attempt, I would keep the spec to roughly half that length.

**Guidelines did not prevent all bugs.** Despite the structured approach, one bug in the Week 13 app was hard enough that GPT-4.1 could not resolve it, and I had to switch to Claude Code to fix it. Upfront planning reduces friction but does not eliminate it.

---

## 7. Reflection

In Week 2, my mental model was that the AI is a fast typist: I tell it what to build, it writes the code, and I fix whatever breaks. The interaction was reactive: generate, encounter bug, ask to fix, repeat. This worked, and I shipped all features, but the session felt like a series of small firefights.

By Week 13, my mental model shifted: the AI is a contractor who performs dramatically better when given a clear brief. The time I spent on planning documents before writing code was not "lost" coding time. It was the most leveraged time in the entire session. The LLM generated more correct code on the first pass, I spent less time debugging, and the codebase came out more consistent.

The biggest surprise was how much the instruction file mattered. It is a short document, but it solved an entire category of problems (environment setup, test commands, architectural context) that consumed significant time in Week 2. It is the single practice I would recommend to anyone starting AI-assisted development.

If I built the app a third time, I would change two things. First, I would keep the planning spec shorter and more focused. The implementation spec had useful content buried in too much detail, some of it duplicated. A tighter spec covering endpoint contracts and edge cases would have been sufficient. Second, I would allocate explicit time for reviewing the frontend code. In both weeks, the backend got careful attention while the frontend was largely accepted as generated. For a real project, that imbalance would be risky.

---

## 8. AI Use Acknowledgement

| Tool | Where Used | How Used |
|------|-----------|----------|
| GitHub Copilot (GPT-4.1) | Week 2 app, Week 13 app | Primary development tool for both apps: conversational code generation, planning, and debugging via Copilot Chat |
| Claude Code | Week 13 app (bug fix only) | Used to resolve one hard bug that GPT-4.1 could not fix |
| Claude Code | This report | I wrote the initial draft; Claude Code structured, polished, and expanded it based on my notes and the codebase |

---

## References

- [1] CS 846 Weekly Guidelines documents (Weeks 4, 5, 6, 8, 10, 11, 12) — full guideline sets developed by student teams