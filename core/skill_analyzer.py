# core/skill_analyzer.py

from ai.gemini_client import ask_gemini


def analyze_skill_gap(career: str, user_skills: list) -> dict:

    user_skills_text = "\n".join([f"- {s}" for s in user_skills]) \
        if user_skills else "- None listed"

    prompt = f"""
You are a career skills expert.

Target career: {career}

Skills the user already has:
{user_skills_text}

Based on what is needed for {career}, identify:
1. Which of their skills are directly relevant
2. What important skills they are still missing

Reply in EXACTLY this format:

EXISTING_SKILLS:
- skill 1
- skill 2

MISSING_SKILLS:
- skill 1
- skill 2
- skill 3
- skill 4
- skill 5

List only the most important ones. Keep each skill under 5 words.
"""

    response = ask_gemini(prompt)
    return parse_skill_gap(response)


def parse_skill_gap(response: str) -> dict:

    existing = []
    missing  = []
    current_section = None

    for line in response.strip().split("\n"):
        line = line.strip()
        if "EXISTING_SKILLS:" in line:
            current_section = "existing"
        elif "MISSING_SKILLS:" in line:
            current_section = "missing"
        elif (line.startswith("-") or line.startswith("*")) and current_section:
            skill = line.lstrip("-* ").strip()
            if skill:
                if current_section == "existing":
                    existing.append(skill)
                else:
                    missing.append(skill)

    return {"existing": existing, "missing": missing}