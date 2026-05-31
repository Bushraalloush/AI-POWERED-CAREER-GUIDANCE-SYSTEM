# app.py

import streamlit as st
from ui.pages.quiz_page import render_quiz
from ui.pages.results_page import render_results
from ui.pages.skills_page import render_skills_assessment
from ui.pages.chat_page import render_chat
from ui.components.styles import apply_custom_styles
from ai.gemini_client import get_current_provider
from sessions.session_manager import (
    save_session,
    get_all_sessions,
    load_session,
    restore_session
)

st.set_page_config(
    page_title="Career Guidance System",
    page_icon=":dart:",
    layout="wide",
    initial_sidebar_state="collapsed"
)

apply_custom_styles()

# --- Header ---
st.markdown("## Career Guidance System")
st.caption("Discover the career path built for your strengths and goals.")

provider = get_current_provider()
if provider != "None":
    st.caption(f"AI Provider: {provider}")

st.divider()

# --- Routing ---
has_matches  = bool(st.session_state.get("career_matches"))
has_skills   = "user_skills" in st.session_state
show_results = st.session_state.get("show_results", False)

# ── Results Page ───────────────────────────────────────
if show_results:

    # Save session
    st.markdown("### Save Your Results")
    col1, col2 = st.columns([2, 1])
    with col1:
        save_name = st.text_input(
            "Name",
            placeholder="Enter your name to save results",
            label_visibility="collapsed"
        )
    with col2:
        if st.button("Save Session", type="primary"):
            if save_name.strip():
                success = save_session(save_name.strip())
                if success:
                    st.success(f"Saved successfully.")
                else:
                    st.error("Save failed. Check terminal.")
            else:
                st.warning("Enter your name first.")

    st.divider()

    tab1, tab2 = st.tabs(["Results", "Career Advisor Chat"])
    with tab1:
        render_results()
    with tab2:
        render_chat()

# ── Skills Assessment ──────────────────────────────────
elif has_matches and not has_skills:
    render_skills_assessment()

# ── Quiz / Landing Page ────────────────────────────────
else:
    # Load previous session — shown before quiz starts
    sessions = get_all_sessions()

    if sessions and not st.session_state.get("quiz_started"):
        st.markdown("### Load a Previous Session")

        options = {
            f"{s['name']} — {s['date']} (Top: {s['top_career']})": s["filename"]
            for s in sessions
        }

        selected = st.selectbox(
            "Choose a saved session",
            options=["— Select a session —"] + list(options.keys())
        )

        if selected != "— Select a session —":
            if st.button("Load Selected Session", type="primary"):
                data = load_session(options[selected])
                if data:
                    restore_session(data)
                    st.success("Session loaded.")
                    st.rerun()
                else:
                    st.error("Could not load session.")

        st.markdown("**— or start a new assessment below —**")
        st.divider()

    render_quiz()
