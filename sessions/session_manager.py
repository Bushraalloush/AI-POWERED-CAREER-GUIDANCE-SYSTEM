# sessions/session_manager.py

import json
import os
from datetime import datetime

# Use current working directory — always the project root
# when running with: streamlit run app.py
BASE_DIR     = os.getcwd()
SESSIONS_DIR = os.path.join(BASE_DIR, "sessions", "data")


def save_session(name: str) -> bool:
    import streamlit as st

    session_data = {
        "name":           name,
        "date":           datetime.now().strftime("%Y-%m-%d %H:%M"),
        "profile":        st.session_state.get("profile", {}),
        "career_matches": st.session_state.get("career_matches", []),
        "user_skills":    st.session_state.get("user_skills", []),
        "answers":        st.session_state.get("answers", {})
    }

    filename = f"{name.lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
    filepath = os.path.join(SESSIONS_DIR, filename)

    try:
        os.makedirs(SESSIONS_DIR, exist_ok=True)
        with open(filepath, "w") as f:
            json.dump(session_data, f, indent=2)
        print(f"✅ Saved to: {filepath}")
        return True
    except Exception as e:
        print(f"❌ Save error: {e}")
        return False


def load_session(filename: str) -> dict:
    filepath = os.path.join(SESSIONS_DIR, filename)
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Load error: {e}")
        return {}


def get_all_sessions() -> list:
    sessions = []

    print(f"Looking for sessions in: {SESSIONS_DIR}")

    if not os.path.exists(SESSIONS_DIR):
        print("Sessions directory does not exist")
        return sessions

    for filename in os.listdir(SESSIONS_DIR):
        if filename.endswith(".json"):
            filepath = os.path.join(SESSIONS_DIR, filename)
            try:
                with open(filepath, "r") as f:
                    data = json.load(f)

                matches     = data.get("career_matches", [])
                top_career  = matches[0][0] if matches else "Unknown"

                sessions.append({
                    "filename":   filename,
                    "name":       data.get("name", "Unknown"),
                    "date":       data.get("date", "Unknown"),
                    "top_career": top_career
                })
            except Exception as e:
                print(f"❌ Error reading {filename}: {e}")
                continue

    sessions.sort(key=lambda x: x["date"], reverse=True)
    print(f"Found {len(sessions)} sessions")
    return sessions


def restore_session(session_data: dict):
    import streamlit as st

    st.session_state.profile        = session_data.get("profile", {})
    st.session_state.career_matches = session_data.get("career_matches", [])
    st.session_state.user_skills    = session_data.get("user_skills", [])
    st.session_state.answers        = session_data.get("answers", {})
    st.session_state.quiz_complete  = True
    st.session_state.quiz_started   = True
    st.session_state.show_results   = True

    keys_to_clear = ["explanations", "skill_checklist"]
    for key in keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]