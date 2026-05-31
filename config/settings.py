# config/settings.py

import os
from dotenv import load_dotenv

load_dotenv()


def _get_secret(key: str) -> str:
    """
    Gets a secret from environment variables first, then Streamlit secrets.
    This makes the app work both locally (.env file) and on Streamlit Cloud (st.secrets).
    """
    # 1. Try environment variable (works locally with .env)
    value = os.getenv(key)
    if value:
        return value

    # 2. Try Streamlit secrets (works on Streamlit Cloud)
    try:
        import streamlit as st
        return st.secrets.get(key, "")
    except Exception:
        return ""


GROQ_API_KEY     = _get_secret("GROQ_API_KEY")
CEREBRAS_API_KEY = _get_secret("CEREBRAS_API_KEY")

APP_NAME    = "AI Career Guidance System"
APP_VERSION = "1.0.0"
