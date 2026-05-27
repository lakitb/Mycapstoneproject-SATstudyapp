# SAT Study App

A Flask-based SAT practice app for Math and Reading/Writing categories.  
Questions are rendered from an in-memory data model and served one at a time with instant feedback.

## Features

- Category selection from homepage
- Difficulty selection (Easy, Medium, Hard)
- Randomized question order per quiz session
- One-question-at-a-time quiz flow
- 5-minute quiz timer with automatic submission at timeout
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

## Deploy

This project is deployment-ready for platforms that support `Procfile` (for example, Render or Railway).

### Generic deployment steps

1. Push this repository to GitHub.
2. Create a new web service in your hosting platform and connect the repo.
3. Configure:
   - Build command: `pip install -r requirements.txt`
   - Start command: `gunicorn wsgi:app`
4. Set environment variables:
   - `FLASK_ENV=production`
5. Deploy and open the generated service URL.

## Project layout

- `run.py`: Flask entry point
- `app/__init__.py`: app factory
- `app/routes.py`: request/response flow
- `app/data.py`: in-memory SAT question bank
- `app/quiz.py`: quiz logic helpers
- `app/templates/`: Jinja templates
- `app/static/styles.css`: responsive styling
- `tests/`: automated tests
