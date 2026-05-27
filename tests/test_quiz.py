from app.data import QUESTION_BANK
from app.quiz import filter_questions, summarize_results


def test_filter_questions_by_category():
    math_questions = filter_questions(QUESTION_BANK, "math")
    assert math_questions
    assert all(question["category"] == "math" for question in math_questions)


def test_summarize_results_counts_correct_and_missed():
    questions = [
        {
            "id": "q1",
            "text": "Question 1",
            "correct_answer": "A",
            "explanation": "Because A.",
        },
        {
            "id": "q2",
            "text": "Question 2",
            "correct_answer": "B",
            "explanation": "Because B.",
        },
    ]
    responses = {"q1": "A", "q2": "C"}

    summary = summarize_results(questions, responses)

    assert summary["total"] == 2
    assert summary["correct"] == 1
    assert summary["incorrect"] == 1
    assert summary["percent"] == 50.0
    assert len(summary["missed"]) == 1
    assert summary["missed"][0]["id"] == "q2"
