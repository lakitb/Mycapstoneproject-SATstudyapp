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
