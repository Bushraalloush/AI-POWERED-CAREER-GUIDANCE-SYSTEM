# core/career_trend.py

from ai.gemini_client import ask_gemini


def get_career_trend(career: str) -> dict:
    """
    Returns market trend data for a given career.
    """

    prompt = f"""
You are a labor market analyst.

Analyze the job market trend for: {career}

Reply in EXACTLY this format, nothing else:

DIRECTION: Growing Rapidly / Growing / Stable / Declining
DEMAND: Very High / High / Moderate / Low
OUTLOOK: Next 5-10 years outlook in one sentence.
DRIVER: The main factor driving this trend in one sentence.
AUTOMATION_RISK: Low / Medium / High
"""

    response = ask_gemini(prompt)
    return parse_trend(response)


def parse_trend(response: str) -> dict:

    result = {
        "direction":        "Unknown",
        "demand":           "Unknown",
        "outlook":          "",
        "driver":           "",
        "automation_risk":  "Unknown"
    }

    for line in response.strip().split("\n"):
        line = line.strip()

        if line.startswith("DIRECTION:"):
            result["direction"] = line.replace("DIRECTION:", "").strip()

        elif line.startswith("DEMAND:"):
            result["demand"] = line.replace("DEMAND:", "").strip()

        elif line.startswith("OUTLOOK:"):
            result["outlook"] = line.replace("OUTLOOK:", "").strip()

        elif line.startswith("DRIVER:"):
            result["driver"] = line.replace("DRIVER:", "").strip()

        elif line.startswith("AUTOMATION_RISK:"):
            result["automation_risk"] = line.replace("AUTOMATION_RISK:", "").strip()

    return result