# core/career_matcher.py

from ai.gemini_client import ask_gemini
from core.profiler import format_profile_for_ai

CAREERS = [
    "Software Engineer",
    "Data Scientist",
    "UX/UI Designer",
    "Product Manager",
    "Cybersecurity Analyst",
    "Business Analyst",
    "Doctor / Medical Professional",
    "Psychologist / Counselor",
    "Mechanical Engineer",
    "Content Creator / Writer"
]


def match_careers(profile: dict) -> list:

    profile_text = format_profile_for_ai(profile)
    careers_list = "\n".join([f"- {c}" for c in CAREERS])

    prompt = f"""
You are a career guidance expert. Score each career for this user.

{profile_text}

Careers:
{careers_list}

For each career reply in EXACTLY this format, one per line:
Career Name: overall | interests | skills | workstyle | values

Example:
Software Engineer: 87 | 90 | 85 | 88 | 82

Score each number 0-100. No extra text.
"""

    response = ask_gemini(prompt)
    return parse_career_scores(response)


def parse_career_scores(response: str) -> list:

    if response.startswith("ERROR:"):
        return []

    results = []

    for line in response.strip().split("\n"):
        if ":" in line and "|" in line:
            try:
                # Split "Software Engineer: 87 | 90 | 85 | 88 | 82"
                career_part, scores_part = line.split(":", 1)
                career = career_part.strip()

                scores = [s.strip() for s in scores_part.split("|")]

                overall    = int(scores[0])
                interests  = int(scores[1]) if len(scores) > 1 else overall
                skills     = int(scores[2]) if len(scores) > 2 else overall
                work_style = int(scores[3]) if len(scores) > 3 else overall
                values     = int(scores[4]) if len(scores) > 4 else overall

                if 0 <= overall <= 100 and len(career) > 3:
                    results.append((career, overall, {
                        "interests":   interests,
                        "skills":      skills,
                        "work_style":  work_style,
                        "values":      values
                    }))
            except (ValueError, IndexError):
                continue

    results.sort(key=lambda x: x[1], reverse=True)
    return results
