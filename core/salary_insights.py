# core/salary_insights.py

from ai.gemini_client import ask_gemini


def get_salary_insights(career: str) -> dict:
    """
    Returns salary ranges and top hiring companies
    for a given career. Results are cached in session state.
    """

    prompt = f"""
You are a career compensation expert.

Provide realistic salary information for: {career}

Reply in EXACTLY this format, nothing else:

ENTRY: $X,000 - $X,000
MID: $X,000 - $X,000
SENIOR: $X,000 - $X,000
COMPANIES: Company1, Company2, Company3, Company4, Company5
NOTES: One sentence about salary factors or growth potential.
"""

    response = ask_gemini(prompt)
    return parse_salary(response)


def parse_salary(response: str) -> dict:

    result = {
        "entry":     "Not available",
        "mid":       "Not available",
        "senior":    "Not available",
        "companies": [],
        "notes":     ""
    }

    for line in response.strip().split("\n"):
        line = line.strip()

        if line.startswith("ENTRY:"):
            result["entry"] = line.replace("ENTRY:", "").strip()

        elif line.startswith("MID:"):
            result["mid"] = line.replace("MID:", "").strip()

        elif line.startswith("SENIOR:"):
            result["senior"] = line.replace("SENIOR:", "").strip()

        elif line.startswith("COMPANIES:"):
            companies_str = line.replace("COMPANIES:", "").strip()
            result["companies"] = [
                c.strip() for c in companies_str.split(",")
            ]

        elif line.startswith("NOTES:"):
            result["notes"] = line.replace("NOTES:", "").strip()

    return result