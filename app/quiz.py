from __future__ import annotations

import random
from typing import Any


def filter_questions(questions: list[dict[str, Any]], category: str) -> list[dict[str, Any]]:
    return [q for q in questions if q.get("category") == category]


def shuffled_question_ids(questions: list[dict[str, Any]]) -> list[str]:
    ids = [q["id"] for q in questions]
    random.shuffle(ids)
    return ids


def get_question_by_id(
    questions: list[dict[str, Any]], question_id: str
) -> dict[str, Any] | None:
    for question in questions:
        if question.get("id") == question_id:
            return question
    return None


def grade_answer(question: dict[str, Any], selected_choice: str) -> bool:
    return question.get("correct_answer") == selected_choice


def summarize_results(
    questions: list[dict[str, Any]], responses: dict[str, str]
) -> dict[str, Any]:
    correct = 0
    missed = []

    for question in questions:
        qid = question["id"]
        selected = responses.get(qid)
        is_correct = selected == question.get("correct_answer")
        if is_correct:
            correct += 1
            continue
        missed.append(
            {
                "id": qid,
                "text": question.get("text"),
                "selected": selected,
                "correct_answer": question.get("correct_answer"),
                "explanation": question.get("explanation"),
            }
        )

    total = len(questions)
    percent = round((correct / total) * 100, 1) if total else 0.0
    return {
        "total": total,
        "correct": correct,
        "incorrect": total - correct,
        "percent": percent,
        "missed": missed,
    }
