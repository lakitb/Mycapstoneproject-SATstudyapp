import time

from app import create_app


def test_homepage_loads():
    app = create_app()
    app.testing = True
    client = app.test_client()

    response = client.get("/")
    assert response.status_code == 200
    assert b"Choose a Quiz Category" in response.data


def test_invalid_category_returns_400():
    app = create_app()
    app.testing = True
    client = app.test_client()

    response = client.post("/start", data={"category": "science"})
    assert response.status_code == 400
    assert b"Invalid category" in response.data


def test_quiz_flow_reaches_results():
    app = create_app()
    app.testing = True
    client = app.test_client()

    start = client.post("/start", data={"category": "math"}, follow_redirects=True)
    assert start.status_code == 200
    assert b"Question 1 of" in start.data

    # Submit answer for first question.
    submit = client.post("/quiz", data={"action": "submit", "choice": "5"}, follow_redirects=True)
    assert submit.status_code == 200
    assert b"Correct!" in submit.data or b"Not quite." in submit.data

    # Continue until results page.
    for _ in range(5):
        next_response = client.post("/quiz", data={"action": "next"}, follow_redirects=True)
        if b"Quiz Complete" in next_response.data:
            break
        client.post("/quiz", data={"action": "submit", "choice": "A"}, follow_redirects=True)
    else:
        raise AssertionError("Quiz did not reach results page")


def test_difficulty_selection_changes_quiz_pool():
    app = create_app()
    app.testing = True
    client = app.test_client()

    response = client.post(
        "/start",
        data={"category": "math", "difficulty": "hard"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Question 1 of 1" in response.data
    assert b"Hard" in response.data


def test_timer_expiry_redirects_to_results():
    app = create_app()
    app.testing = True
    client = app.test_client()

    client.post("/start", data={"category": "math", "difficulty": "easy"})
    with client.session_transaction() as session_state:
        session_state["quiz"]["deadline_epoch"] = int(time.time()) - 1
        session_state.modified = True

    response = client.get("/quiz", follow_redirects=True)
    assert response.status_code == 200
    assert b"Quiz Complete" in response.data
    assert b"Time expired" in response.data


def test_invalid_difficulty_returns_400():
    app = create_app()
    app.testing = True
    client = app.test_client()

    response = client.post("/start", data={"category": "math", "difficulty": "expert"})
    assert response.status_code == 400
    assert b"Invalid difficulty" in response.data


def test_unknown_route_uses_safe_fallback_page():
    app = create_app()
    app.testing = True
    client = app.test_client()

    response = client.get("/not-a-real-route")
    assert response.status_code == 404
    assert b"Page not found" in response.data
