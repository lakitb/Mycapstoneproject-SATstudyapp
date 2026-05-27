QUESTION_BANK = [
    {
        "id": "math_1",
        "category": "math",
        "difficulty": "easy",
        "text": "If 3x + 5 = 20, what is the value of x?",
        "choices": ["3", "4", "5", "6"],
        "correct_answer": "5",
        "explanation": "Subtract 5 from both sides to get 3x = 15, then divide by 3.",
    },
    {
        "id": "math_2",
        "category": "math",
        "difficulty": "medium",
        "text": "A circle has radius 4. What is its area?",
        "choices": ["8pi", "16pi", "32pi", "64pi"],
        "correct_answer": "16pi",
        "explanation": "Use A = pi r^2, so A = pi * 4^2 = 16pi.",
    },
    {
        "id": "math_3",
        "category": "math",
        "difficulty": "hard",
        "text": "If f(x) = 2x^2 - 3x + 1, what is f(3)?",
        "choices": ["8", "10", "12", "14"],
        "correct_answer": "10",
        "explanation": "f(3) = 2(9) - 3(3) + 1 = 18 - 9 + 1 = 10.",
    },
    {
        "id": "reading_1",
        "category": "reading_writing",
        "difficulty": "easy",
        "text": "Choose the best transition: 'Lena studied hard; ___, she passed the exam.'",
        "choices": ["however", "therefore", "meanwhile", "instead"],
        "correct_answer": "therefore",
        "explanation": "The second clause is a result of the first, so 'therefore' fits.",
    },
    {
        "id": "reading_2",
        "category": "reading_writing",
        "difficulty": "medium",
        "text": "Which revision is most concise and clear? 'The reason is because it was late.'",
        "choices": [
            "The reason is because it was late.",
            "It was late.",
            "The reason was due to lateness.",
            "Because it was late was the reason.",
        ],
        "correct_answer": "It was late.",
        "explanation": "The original phrase is redundant; the concise sentence is best.",
    },
    {
        "id": "reading_3",
        "category": "reading_writing",
        "difficulty": "hard",
        "text": "Which choice best maintains formal tone? 'The scientist was super into the results.'",
        "choices": [
            "The scientist was super into the results.",
            "The scientist was highly interested in the results.",
            "The scientist totally liked the results.",
            "The scientist got really pumped about the results.",
        ],
        "correct_answer": "The scientist was highly interested in the results.",
        "explanation": "Formal writing avoids slang like 'super into' or 'totally liked.'",
    },
]


VALID_CATEGORIES = {"math", "reading_writing"}
VALID_DIFFICULTIES = {"easy", "medium", "hard"}
