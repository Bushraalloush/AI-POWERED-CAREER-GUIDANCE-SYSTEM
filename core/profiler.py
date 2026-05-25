# core/profiler.py

def build_profile(answers: dict) -> dict:
    """
    Takes the raw quiz answers and builds a clean user profile.
    This profile is what gets sent to the AI for career matching.
    """

    profile = {
        "interests": [],
        "skills": [],
        "work_style": [],
        "values": [],
        "raw_answers": answers
    }

    for key, data in answers.items():
        dimension = data["dimension"]
        answer = data["answer"]

        if dimension == "interests":
            profile["interests"].append(answer)

        elif dimension == "skills":
            profile["skills"].append(answer)

        elif dimension == "work_style":
            profile["work_style"].append(answer)

        elif dimension == "values":
            profile["values"].append(answer)

    return profile


def format_profile_for_ai(profile: dict) -> str:
    """
    Converts the profile dictionary into a readable text
    that we can send to Gemini as part of a prompt.
    """

    return f"""
User Profile:
- Interests: {', '.join(profile['interests'])}
- Skills & Strengths: {', '.join(profile['skills'])}
- Work Style: {', '.join(profile['work_style'])}
- Core Values: {', '.join(profile['values'])}
"""