# CLAUDE.md

## Project architecture

- Framework: Flask (server-rendered HTML with Jinja templates)
- Entry point: `run.py`
- Application factory: `app/__init__.py`
- Routes/controller layer: `app/routes.py`
- Domain logic utilities: `app/quiz.py`
- In-memory question data source: `app/data.py`
- UI templates: `app/templates/`
- Static styling assets: `app/static/`
- Automated tests: `tests/`

## Coding patterns

- Keep routes thin: request parsing + response rendering only.
- Put quiz state transformation in pure functions inside `app/quiz.py`.
- Use in-memory data (`QUESTION_BANK`) for local development; preserve stable question `id`.
- Template rendering must come from structured data, not hardcoded HTML question content.
- Favor explicit names over abbreviations for readability.
- Add small, focused helper functions rather than one large view function.

## Session and state conventions

- Session key: `quiz`
- Session payload shape:
  - `category` (`math` or `reading_writing`)
  - `difficulty` (`easy`, `medium`, or `hard`)
  - `question_ids` (shuffled list per session)
  - `question_index` (zero-based pointer)
  - `responses` (`{question_id: selected_choice}`)
  - `feedback` (result details for current answered question)
  - `deadline_epoch` (quiz timeout)
  - `timed_out` (timer expiration flag)
- Clear `quiz` session state after results render.

## Constraints and guardrails

- Validate category and difficulty before quiz starts.
- Handle missing/invalid session by redirecting to homepage.
- Handle missing question data with safe fallback error page.
- Handle unknown routes with a non-crashing fallback page.
- Keep code ASCII unless existing file already requires Unicode.
- Avoid introducing new dependencies unless necessary.

## Testing expectations

- Test pure quiz helpers (`filter_questions`, grading, summaries).
- Test route flow: homepage, start quiz, submit answer, next question, results.
- Ensure invalid category and empty-session paths do not crash.
