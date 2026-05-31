# core/interview_prep.py

from ai.gemini_client import ask_gemini


def get_interview_questions(career: str, user_skills: list) -> list:
    """
    Generates likely interview questions for a career
    with answering tips tailored to the user's profile.
    """

    skills_text = ", ".join(user_skills[:5]) if user_skills else "general skills"

    prompt = f"""
You are a hiring manager and interview coach.

Generate interview preparation for: {career}

The candidate's current skills include: {skills_text}

Provide exactly 5 interview questions with answering tips.

Reply in EXACTLY this format, repeat for all 5 questions:

QUESTION: The interview question here?
TIP: One specific tip on how to answer this question well.

---

QUESTION: Next question?
TIP: Tip for this question.

---

Make questions realistic and specific to the role.
Tips should be actionable, not generic.
"""

    response = ask_gemini(prompt)
    return parse_questions(response)


def parse_questions(response: str) -> list:

    questions = []
    current   = {}

    for line in response.strip().split("\n"):
        line = line.strip()

        if line.startswith("QUESTION:"):
            if current.get("question"):
                questions.append(current)
                current = {}
            current["question"] = line.replace("QUESTION:", "").strip()

        elif line.startswith("TIP:"):
            current["tip"] = line.replace("TIP:", "").strip()

    if current.get("question"):
        questions.append(current)

    return questions[:5]
