# SAT Study App

A Flask-based SAT practice app for Math and Reading/Writing categories.  
Questions are rendered from an in-memory data model and served one at a time with instant feedback.

## Features

- Category selection from homepage
- Randomized question order per quiz session
- One-question-at-a-time quiz flow
- Instant correctness feedback and explanation
- Final results summary with score, percentage, and missed question review

## Run locally

1. Create a virtual environment:
   - `python3 -m venv .venv`
2. Activate it:
   - macOS/Linux: `source .venv/bin/activate`
3. Install dependencies:
   - `pip install -r requirements.txt`
4. Start the app:
   - `python run.py`
5. Open:
   - `http://127.0.0.1:5000`

## Run tests

- `pytest`

## Project layout

- `run.py`: Flask entry point
- `app/__init__.py`: app factory
- `app/routes.py`: request/response flow
- `app/data.py`: in-memory SAT question bank
- `app/quiz.py`: quiz logic helpers
- `app/templates/`: Jinja templates
- `app/static/styles.css`: responsive styling
- `tests/`: automated tests
