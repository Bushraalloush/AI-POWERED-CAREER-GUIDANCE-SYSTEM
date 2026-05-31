# ai/gemini_client.py

import groq as groq_lib
import cerebras.cloud.sdk as cerebras_lib

# ── Model names ────────────────────────────────────────────────────────────────
GROQ_MODEL     = "llama-3.3-70b-versatile"
CEREBRAS_MODEL = "llama3.3-70b"          # NOTE: no dashes in version number

# ── Provider tracking ──────────────────────────────────────────────────────────
current_provider = "None"


def _get_groq_client():
    """
    Creates a Groq client lazily (only when a function actually needs it).
    This prevents a crash at import time when API keys are not yet available.
    """
    from config.settings import GROQ_API_KEY
    if not GROQ_API_KEY:
        raise ValueError(
            "GROQ_API_KEY is missing. "
            "Add it to your .env file locally or to Streamlit secrets in the cloud."
        )
    return groq_lib.Groq(api_key=GROQ_API_KEY)


def _get_cerebras_client():
    """
    Creates a Cerebras client lazily (only when a function actually needs it).
    """
    from config.settings import CEREBRAS_API_KEY
    if not CEREBRAS_API_KEY:
        raise ValueError(
            "CEREBRAS_API_KEY is missing. "
            "Add it to your .env file locally or to Streamlit secrets in the cloud."
        )
    return cerebras_lib.Cerebras(api_key=CEREBRAS_API_KEY)


def ask_roq(prompt: str, system_prompt: str = "") -> str:
    """
    Calls the Groq API. Supports an optional system prompt.
    """
    client = _get_groq_client()

    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=messages,
        max_tokens=1024,
        temperature=0.7,
    )
    return response.choices[0].message.content


def ask_cerebras(prompt: str, system_prompt: str = "") -> str:
    """
    Calls the Cerebras API as a fallback.
    """
    client = _get_cerebras_client()

    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    response = client.chat.completions.create(
        model=CEREBRAS_MODEL,
        messages=messages,
        max_tokens=1024,
    )
    return response.choices[0].message.content


def ask_gemini(prompt: str, system_prompt: str = "") -> str:
    """
    Main AI call function. Tries Groq first, falls back to Cerebras.
    Returns an ERROR: prefixed string on total failure.

    The name 'ask_gemini' is kept for backwards compatibility with the rest
    of the codebase — the underlying providers are Groq and Cerebras.
    """
    global current_provider

    # ── Try Groq ───────────────────────────────────────────────────────────────
    try:
        client = _get_groq_client()
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=messages,
            max_tokens=1024,
            temperature=0.7,
        )
        current_provider = "Groq ⚡"
        return response.choices[0].message.content

    except groq_lib.RateLimitError:
        pass  # Fall through to Cerebras

    except groq_lib.AuthenticationError:
        current_provider = "None ❌"
        return "ERROR: Groq API key is invalid. Please check your secrets."

    except groq_lib.APIConnectionError:
        pass  # Network issue — try Cerebras

    except Exception:
        pass  # Any other Groq error — fall through

    # ── Try Cerebras fallback ──────────────────────────────────────────────────
    try:
        client = _get_cerebras_client()
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        response = client.chat.completions.create(
            model=CEREBRAS_MODEL,
            messages=messages,
            max_tokens=1024,
        )
        current_provider = "Cerebras 🔵"
        return response.choices[0].message.content

    except Exception as cerebras_error:
        current_provider = "None ❌"
        error_msg = str(cerebras_error).lower()

        if "rate limit" in error_msg:
            return "ERROR: Rate limit reached on all providers. Please wait 60 seconds and try again."
        if "api_key" in error_msg or "authentication" in error_msg:
            return "ERROR: API key invalid. Please check your Groq and Cerebras secrets."
        return "ERROR: AI service temporarily unavailable. Please try again in a moment."


def ask_chat(messages: list) -> str:
    """
    Chat-specific AI call that accepts a properly structured messages list:
    [
        {"role": "system",    "content": "You are a career advisor..."},
        {"role": "user",      "content": "What career suits me?"},
        {"role": "assistant", "content": "Based on your profile..."},
        {"role": "user",      "content": "What should I learn first?"}
    ]

    This gives significantly better responses than ask_gemini() for conversations
    because the LLM correctly reads the system context and conversation history
    in the roles they were designed for.
    """
    global current_provider

    # ── Try Groq ───────────────────────────────────────────────────────────────
    try:
        client = _get_groq_client()
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=messages,
            max_tokens=1024,
            temperature=0.7,
        )
        current_provider = "Groq ⚡"
        return response.choices[0].message.content

    except groq_lib.RateLimitError:
        pass  # Fall through to Cerebras

    except groq_lib.AuthenticationError:
        current_provider = "None ❌"
        return "ERROR: groq API key is invalid."

    except Exception:
        pass

    # ── Try Cerebras fallback ──────────────────────────────────────────────────
    try:
        client = _get_cerebras_client()
        response = client.chat.completions.create(
            model=CEREBRAS_MODEL,
            messages=messages,
            max_tokens=1024,
        )
        current_provider = "Cerebras 🔵"
        return response.choices[0].message.content

    except Exception:
        current_provider = "None ❌"
        return "ERROR: AI service temporarily unavailable. Please wait a moment and try again."


def get_current_provider() -> str:
    return current_provider
