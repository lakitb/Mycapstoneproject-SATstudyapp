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

## AI Workflow
I took a different approach with my tools, using the right one for each job instead of relying on just one. When I was planning, I started with `ReadFile` to get a sense of the existing structure - things like routes, templates, tests, and docs. This helped me make task proposals that fit with how the app already worked, rather than just making assumptions. As a result, I didn't have to redo as much work because I could line up new changes with the app's current session model and template flow. When it came time to execute, `ApplyPatch` was my go-to tool. It helped me make focused changes, kept my edits small and manageable, and made it easy to see exactly what had changed with each task. For polishing, I used `ReadLints` along with some small tweaks to the CSS and templates to improve how the app responded and how accessible it was, all without messing up the quiz logic. Finally, when I was reviewing and verifying everything, `Shell` was the last check: I ran full `pytest` tests, checked that the server started up okay, did some smoke tests with gunicorn, and even ran through some manual tests to make sure everything was working as it should.

There was a moment when `ApplyPatch` clearly outperformed shell-based editing, especially when it came to making updates to multiple files in Flask and Jinja. The reason for this was that `ApplyPatch` used context hunks, which reduced the number of accidental edits and made the review process much faster. On the other hand, I used the wrong tool when I was doing manual end-to-end verification. At first, I tried using `curl -L` for POST redirect flows, but it didn't work well in this particular stateful quiz sequence. So, I switched to a short Python script that used `urllib` and handled cookies, and that gave me reliable end-to-end validation for a variety of scenarios, including happy path, wrong answers, invalid inputs, and empty-session behavior. This switch made a big difference and helped me get the results I needed.

#Reflection essay
1) This project introduced me to a more awake idea of how to be efficient with an agentic workflow, rather than giving me a specific idea of all the details needed in each of my own codes. With normal 4 hours I'd have been able to build an application with only static pages and basic features for creating a SAT Quiz. With AI, I was able to take my thinking to the next level, and add in random question sequences, difficulty filtering, score tracking, UI tidying up, among other features, in much less time than it would take me to do this on my own. Increased not to get bogged down in boilerplate or repetitive implementation details was the largest gain. The only reason I wear to the wire to draw routes and sort out silly syntax errors is because I don't have to do it, I can just explain my intention and try it again and again.
2) However, there were some instances in which I had to press back against Claude to get the code to do exactly what I needed it to do rather than “working code”. It was one of the examples of 'scope control'. Sometimes, Claude will add in other layers of abstraction or auxiliary functions, or further layers of validation that don't actually need for the project. Was constantly pushing it back to simpler implementations that would add to the time constraints and on board application architecture. If UI behaviour did not even follow a notion of "correct" from the user's perspective, but code was still correct, I had to take matters into my own hands. It is not easy to write functional interfaces intuitively or motivatively without the guidance of the model for the SAT students.

3) This project is a learning one, it taught me that my sense of judgment is relevant, far more important than having a quick learner doing code. AI can generate code quickly but isn't very good at knowing what to build, what isn't plus where it's cumbersome. There are a lot of things now that I don't know that are no longer syntax-related and they are architecture, prioritization, and evaluation related. Sometimes I accepted solutions that were generated without going as far as developing them myself, such as. Then I started slowing down, looking at the implementation to see if there were any issues, and I gave better instructions, earlier in the game. I learned of the need for more instincts in testing and in state management as well, which are where the bugs were apt to be found.

4) I will tell everyone that I am going to present this workflow professionally and carefully; I will take it with me in my internship. I'd start day one off right by figuring out how the project is set up, what conventions the team is expecting, etc. The time I had to use AI intentionally I'd write in Claude Code for code, plan in Claude Chat, do some quick polish in Copilot then review and analyze side-case in Claude Chat. What I'm learning is that AI should complement human intuition to offer the best results. It's not just coding anymore, it's having to lead the systems, consider the pros and cons and know where to apply the model and when to take some time and think.