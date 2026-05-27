## Task 1 — Difficulty filtering
- Brief: Add Easy/Medium/Hard selection and only serve questions matching category + difficulty.
- What Claude proposed: Extend `filter_questions` with optional difficulty and pass selected difficulty from homepage form into quiz session state.
- What I changed before approving: Added difficulty validation with safe 400 fallback and updated no-question message for category+difficulty combos.
- Verification: Added route + unit tests for difficulty filtering and confirmed quiz renders `Question 1 of 1` for `math + hard`.
- One thing I learned: Result totals must use the exact session question IDs, not all questions in a category.

## Task 2 — Quiz timer
- Brief: Add SAT-style countdown timer and auto-finish behavior when time runs out.
- What Claude proposed: Store a session deadline epoch and compute remaining seconds on each quiz request; redirect to results if expired.
- What I changed before approving: Added client-side timer display/update in `quiz.html` plus timeout banner on the results page.
- Verification: Added a test that forces an expired deadline in session and confirms redirect to results with timeout message.
- One thing I learned: Server-side timeout checks are still required even when a client-side timer exists.

## Task 3 — Automated test expansion
- Brief: Increase tests for filtering, progression, timer behavior, and invalid inputs.
- What Claude proposed: Add focused tests for difficulty filtering, invalid difficulty, timeout handling, and unknown-route fallback.
- What I changed before approving: Kept tests deterministic by setting session deadline directly for timeout checks.
- Verification: `source .venv/bin/activate && pytest` passes for expanded suite.
- One thing I learned: Direct session mutation in Flask tests is an efficient way to test time-based behavior.

## Task 4 — Edge-case safety and conventions updates
- Brief: Handle invalid states cleanly and document new conventions.
- What Claude proposed: Add a global 404 fallback page, update `CLAUDE.md` session schema, and refresh README features.
- What I changed before approving: Included explicit `difficulty`, `deadline_epoch`, and `timed_out` fields in architecture conventions.
- Verification: Added and passed a test for unknown routes and manually reviewed updated docs.
- One thing I learned: Lightweight docs updates during implementation prevent architecture drift.

## Task 5 — Responsive and accessibility polish
- Brief: Improve visual hierarchy and mobile usability without changing core quiz logic.
- What Claude proposed: Add focus-visible states, button interaction polish, spacing consistency, and cleaner missed-question list presentation.
- What I changed before approving: Kept style updates minimal and framework-free so readability and behavior stayed stable.
- Verification: Ran local UI smoke checks on homepage and quiz pages; confirmed forms/buttons remain functional.
- One thing I learned: Small accessibility tweaks (focus outlines + hover states) produce outsized UX improvements.

## Task 6 — Deployment-ready packaging
- Brief: Make the app deployable on a standard Python web host and document the exact setup.
- What Claude proposed: Add `gunicorn`, `wsgi.py`, and `Procfile`, then document build/start commands in README.
- What I changed before approving: Added `runtime.txt` and kept deployment section generic for Render/Railway-style services.
- Verification: Installed updated dependencies, ran `pytest`, and validated `gunicorn wsgi:app` boots successfully.
- One thing I learned: A simple WSGI entrypoint plus explicit start command removes most deployment ambiguity.
