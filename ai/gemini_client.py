# ai/gemini_client.py

from groq import Groq
from cerebras.cloud.sdk import Cerebras
from config.settings import GROQ_API_KEY, CEREBRAS_API_KEY

groq_client     = Groq(api_key=GROQ_API_KEY)
cerebras_client = Cerebras(api_key=CEREBRAS_API_KEY)

GROQ_MODEL     = "llama-3.3-70b-versatile"
CEREBRAS_MODEL = "llama-3.3-70b"

current_provider = "None"


def ask_groq(prompt: str) -> str:
    response = groq_client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1024
    )
    return response.choices[0].message.content


def ask_cerebras(prompt: str) -> str:
    response = cerebras_client.chat.completions.create(
        model=CEREBRAS_MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1024
    )
    return response.choices[0].message.content


def ask_gemini(prompt: str) -> str:
    global current_provider

    try:
        result = ask_groq(prompt)
        current_provider = "Groq ⚡"
        return result

    except Exception as groq_error:
        try:
            result = ask_cerebras(prompt)
            current_provider = "Cerebras 🔵"
            return result

        except Exception as cerebras_error:
            current_provider = "None ❌"
            return f"ERROR: All providers failed.\nGroq: {str(groq_error)}\nCerebras: {str(cerebras_error)}"


def get_current_provider() -> str:
    return current_provider