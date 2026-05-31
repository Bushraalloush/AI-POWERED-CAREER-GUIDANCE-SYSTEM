# core/roadmap_generator.py

from ai.gemini_client import ask_gemini


def generate_roadmap(career: str, missing_skills: list) -> list:
    """
    Generates a phased learning roadmap based on
    the career target and the user's skill gaps.
    Returns a list of phases, each with steps.
    """

    missing_text = "\n".join([f"- {s}" for s in missing_skills]) \
        if missing_skills else "- General foundational skills"

    prompt = f"""
You are a career development expert.

Target career: {career}

Skills the user needs to develop:
{missing_text}

Create a practical 4-phase learning roadmap.
Each phase should build on the previous one.

Reply in EXACTLY this format:

PHASE 1: Foundation
DURATION: 4 weeks
GOAL: One sentence describing this phase goal
STEPS:
- Step one
- Step two
- Step three

PHASE 2: Core Development
DURATION: 2 months
GOAL: One sentence describing this phase goal
STEPS:
- Step one
- Step two
- Step three

PHASE 3: Specialization
DURATION: 3 months
GOAL: One sentence describing this phase goal
STEPS:
- Step one
- Step two
- Step three

PHASE 4: Job Readiness
DURATION: 3 months
GOAL: One sentence describing this phase goal
STEPS:
- Step one
- Step two
- Step three

Be specific and practical. Steps should be concrete actions, not vague advice.
"""

    response = ask_gemini(prompt)
    return parse_roadmap(response)


def parse_roadmap(response: str) -> list:
    """
    Parses the AI response into a structured list of phases.
    Each phase is a dictionary with title, duration, goal, steps.
    """

    phases    = []
    current   = None

    for line in response.strip().split("\n"):
        line = line.strip()

        if line.startswith("PHASE"):
            if current:
                phases.append(current)
            title = line.split(":", 1)[1].strip() if ":" in line else line
            current = {
                "title":    title,
                "duration": "",
                "goal":     "",
                "steps":    []
            }

        elif line.startswith("DURATION:") and current:
            current["duration"] = line.replace("DURATION:", "").strip()

        elif line.startswith("GOAL:") and current:
            current["goal"] = line.replace("GOAL:", "").strip()

        elif (line.startswith("-") or line.startswith("*")) and current:
            step = line.lstrip("-* ").strip()
            if step:
                current["steps"].append(step)

    if current:
        phases.append(current)

    return phases
