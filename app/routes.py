from __future__ import annotations

import time

from flask import Blueprint, redirect, render_template, request, session, url_for

from .data import QUESTION_BANK, VALID_CATEGORIES, VALID_DIFFICULTIES
from .quiz import (
    filter_questions,
    get_question_by_id,
    grade_answer,
    shuffled_question_ids,
    summarize_results,
)

bp = Blueprint("quiz", __name__)
QUIZ_DURATION_SECONDS = 300


@bp.get("/")
def home():
    return render_template("home.html")


@bp.post("/start")
def start_quiz():
    category = request.form.get("category", "")
    difficulty = request.form.get("difficulty", "easy")
    if category not in VALID_CATEGORIES:
        return render_template(
            "error.html",
            title="Invalid category",
            message="Please choose a valid quiz category from the homepage.",
        ), 400

    if difficulty not in VALID_DIFFICULTIES:
        return render_template(
            "error.html",
            title="Invalid difficulty",
            message="Please choose a valid difficulty level from the homepage.",
        ), 400

    questions = filter_questions(QUESTION_BANK, category, difficulty)
    if not questions:
        return render_template(
            "error.html",
            title="No questions available",
            message="No questions were found for this category and difficulty yet.",
        ), 404

    session["quiz"] = {
        "category": category,
        "difficulty": difficulty,
        "question_ids": shuffled_question_ids(questions),
        "question_index": 0,
        "responses": {},
        "feedback": None,
        "deadline_epoch": int(time.time()) + QUIZ_DURATION_SECONDS,
        "timed_out": False,
    }
    return redirect(url_for("quiz.show_quiz"))


@bp.route("/quiz", methods=["GET", "POST"])
def show_quiz():
    quiz_state = session.get("quiz")
    if not quiz_state:
        return redirect(url_for("quiz.home"))

    category = quiz_state["category"]
    difficulty = quiz_state["difficulty"]
    questions = filter_questions(QUESTION_BANK, category, difficulty)
    question_ids = quiz_state["question_ids"]
    question_index = quiz_state["question_index"]
    questions_by_id = {question["id"]: question for question in questions}
    ordered_questions = [
        questions_by_id[question_id] for question_id in question_ids if question_id in questions_by_id
    ]
    remaining_seconds = max(0, quiz_state.get("deadline_epoch", 0) - int(time.time()))

    if remaining_seconds <= 0:
        quiz_state["timed_out"] = True
        session["quiz"] = quiz_state
        return redirect(url_for("quiz.results"))

    if request.method == "POST":
        action = request.form.get("action")
        if action == "submit":
            if question_index >= len(question_ids):
                return redirect(url_for("quiz.results"))

            current_question = get_question_by_id(ordered_questions, question_ids[question_index])
            if current_question is None:
                return render_template(
                    "error.html",
                    title="Question unavailable",
                    message="A quiz question was missing. Please restart the quiz.",
                ), 500

            selected = request.form.get("choice")
            if not selected:
                return render_template(
                    "quiz.html",
                    category=category,
                    difficulty=difficulty,
                    question=current_question,
                    question_number=question_index + 1,
                    total_questions=len(question_ids),
                    error_message="Please select an answer before submitting.",
                    feedback=quiz_state.get("feedback"),
                    remaining_seconds=remaining_seconds,
                )

            is_correct = grade_answer(current_question, selected)
            quiz_state["responses"][current_question["id"]] = selected
            quiz_state["feedback"] = {
                "selected": selected,
                "is_correct": is_correct,
                "correct_answer": current_question["correct_answer"],
                "explanation": current_question["explanation"],
            }
            session["quiz"] = quiz_state

        elif action == "next":
            quiz_state["question_index"] += 1
            quiz_state["feedback"] = None
            session["quiz"] = quiz_state
            if quiz_state["question_index"] >= len(question_ids):
                return redirect(url_for("quiz.results"))

        return redirect(url_for("quiz.show_quiz"))

    question_index = quiz_state["question_index"]
    if question_index >= len(question_ids):
        return redirect(url_for("quiz.results"))

    current_question = get_question_by_id(ordered_questions, question_ids[question_index])
    if current_question is None:
        return render_template(
            "error.html",
            title="Question unavailable",
            message="A quiz question was missing. Please restart the quiz.",
        ), 500

    return render_template(
        "quiz.html",
        category=category,
        difficulty=difficulty,
        question=current_question,
        question_number=question_index + 1,
        total_questions=len(question_ids),
        error_message=None,
        feedback=quiz_state.get("feedback"),
        remaining_seconds=remaining_seconds,
    )


@bp.get("/results")
def results():
    quiz_state = session.get("quiz")
    if not quiz_state:
        return redirect(url_for("quiz.home"))

    category = quiz_state["category"]
    difficulty = quiz_state.get("difficulty")
    questions = filter_questions(QUESTION_BANK, category, difficulty)
    questions_by_id = {question["id"]: question for question in questions}
    ordered_questions = [
        questions_by_id[question_id]
        for question_id in quiz_state.get("question_ids", [])
        if question_id in questions_by_id
    ]
    result = summarize_results(ordered_questions, quiz_state.get("responses", {}))
    result["timed_out"] = quiz_state.get("timed_out", False)
    session.pop("quiz", None)
    return render_template(
        "results.html",
        category=category,
        difficulty=difficulty,
        result=result,
    )
