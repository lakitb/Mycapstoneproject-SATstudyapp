from __future__ import annotations

from flask import Blueprint, redirect, render_template, request, session, url_for

from .data import QUESTION_BANK, VALID_CATEGORIES
from .quiz import (
    filter_questions,
    get_question_by_id,
    grade_answer,
    shuffled_question_ids,
    summarize_results,
)

bp = Blueprint("quiz", __name__)


@bp.get("/")
def home():
    return render_template("home.html")


@bp.post("/start")
def start_quiz():
    category = request.form.get("category", "")
    if category not in VALID_CATEGORIES:
        return render_template(
            "error.html",
            title="Invalid category",
            message="Please choose a valid quiz category from the homepage.",
        ), 400

    questions = filter_questions(QUESTION_BANK, category)
    if not questions:
        return render_template(
            "error.html",
            title="No questions available",
            message="No questions were found for this category yet.",
        ), 404

    session["quiz"] = {
        "category": category,
        "question_ids": shuffled_question_ids(questions),
        "question_index": 0,
        "responses": {},
        "feedback": None,
    }
    return redirect(url_for("quiz.show_quiz"))


@bp.route("/quiz", methods=["GET", "POST"])
def show_quiz():
    quiz_state = session.get("quiz")
    if not quiz_state:
        return redirect(url_for("quiz.home"))

    category = quiz_state["category"]
    questions = filter_questions(QUESTION_BANK, category)
    question_ids = quiz_state["question_ids"]
    question_index = quiz_state["question_index"]

    if request.method == "POST":
        action = request.form.get("action")
        if action == "submit":
            if question_index >= len(question_ids):
                return redirect(url_for("quiz.results"))

            current_question = get_question_by_id(questions, question_ids[question_index])
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
                    question=current_question,
                    question_number=question_index + 1,
                    total_questions=len(question_ids),
                    error_message="Please select an answer before submitting.",
                    feedback=quiz_state.get("feedback"),
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

    current_question = get_question_by_id(questions, question_ids[question_index])
    if current_question is None:
        return render_template(
            "error.html",
            title="Question unavailable",
            message="A quiz question was missing. Please restart the quiz.",
        ), 500

    return render_template(
        "quiz.html",
        category=category,
        question=current_question,
        question_number=question_index + 1,
        total_questions=len(question_ids),
        error_message=None,
        feedback=quiz_state.get("feedback"),
    )


@bp.get("/results")
def results():
    quiz_state = session.get("quiz")
    if not quiz_state:
        return redirect(url_for("quiz.home"))

    category = quiz_state["category"]
    questions = filter_questions(QUESTION_BANK, category)
    result = summarize_results(questions, quiz_state.get("responses", {}))
    session.pop("quiz", None)
    return render_template("results.html", category=category, result=result)
