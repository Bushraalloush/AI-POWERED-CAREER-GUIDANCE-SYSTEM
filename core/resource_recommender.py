# core/resource_recommender.py

import urllib.parse
from ai.gemini_client import ask_gemini


def get_resources_for_skills(career: str, missing_skills: list) -> dict:

    if not missing_skills:
        missing_skills = ["General career skills"]

    skills_text = "\n".join([f"- {s}" for s in missing_skills[:5]])

    prompt = f"""
You are a learning resources expert for career development.

Target career: {career}

Skills to learn:
{skills_text}

Recommend specific, real, currently available learning resources.
Do NOT include any URLs or links.

Reply in EXACTLY this format:

FREE_COURSES:
- Course name | Platform name
- Course name | Platform name
- Course name | Platform name

BOOKS:
- Book title | Author name
- Book title | Author name

PRACTICE_PLATFORMS:
- Platform name | What to practice there
- Platform name | What to practice there

COMMUNITIES:
- Community name | Where to find it
- Community name | Where to find it

Only recommend resources that genuinely exist.
Be specific with course names and book titles.
"""

    response = ask_gemini(prompt)
    return parse_resources(response)


def build_search_url(query: str) -> str:
    """Builds a reliable Google search URL for any resource."""
    return f"https://www.google.com/search?q={urllib.parse.quote(query)}"


def parse_resources(response: str) -> dict:

    resources = {
        "free_courses":       [],
        "books":              [],
        "practice_platforms": [],
        "communities":        []
    }

    current_section = None

    for line in response.strip().split("\n"):
        line = line.strip()

        if "FREE_COURSES:" in line:
            current_section = "free_courses"
        elif "BOOKS:" in line:
            current_section = "books"
        elif "PRACTICE_PLATFORMS:" in line:
            current_section = "practice_platforms"
        elif "COMMUNITIES:" in line:
            current_section = "communities"
        elif (line.startswith("-") or line.startswith("*")) and current_section:
            item = line.lstrip("-* ").strip()
            if item and "|" in item:
                resources[current_section].append(item)

    return resources
