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
    initial_sidebar_state="expanded"
)

apply_custom_styles()

# ── Derive state flags ─────────────────────────────────────────────────────────
has_matches  = bool(st.session_state.get("career_matches"))
has_skills   = "user_skills" in st.session_state
show_results = st.session_state.get("show_results", False)
quiz_started = st.session_state.get("quiz_started", False)
quiz_done    = st.session_state.get("quiz_complete", False)

# active_page controls what shows in the main area when results are ready
# Defaults to "results". Can be set to "chat" from the sidebar.
if "active_page" not in st.session_state:
    st.session_state.active_page = "results"

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:

    # ── Brand ──
    st.markdown("## 🎯 Career Guidance")
    st.caption("AI-powered career discovery")

    # ── AI Status ──
    provider = get_current_provider()
    if provider not in ("None", ""):
        st.markdown(f"🟢 &nbsp; `{provider}`", unsafe_allow_html=True)
    else:
        st.markdown("🔴 &nbsp; `AI Offline`", unsafe_allow_html=True)

    st.divider()

    # ── Navigation ────────────────────────────────────────────────────────────
    #
    # HOW THIS WORKS:
    # Each button sets st.session_state.active_page to a string value.
    # The main content area reads that value and renders accordingly.
    # Buttons are disabled when the section isn't accessible yet.
    #
    st.markdown("### Navigation")

    # -- Quiz --
    quiz_label = "✅ Career Quiz" if quiz_done else ("▶ Career Quiz" if quiz_started else "○ Career Quiz")
    if st.button(quiz_label, key="nav_quiz", use_container_width=True):
        # Only allow going back to quiz via reset (quiz clears all state)
        pass  # Quiz is the starting point; use Reset to go back

    # -- Skills Assessment --
    skills_label = "✅ Skills Assessment" if has_skills else "○ Skills Assessment"
    skills_disabled = not has_matches
    if st.button(skills_label, key="nav_skills", use_container_width=True, disabled=skills_disabled):
        # Navigate back to skills screen
        if "show_results" in st.session_state:
            del st.session_state["show_results"]
        if "user_skills" in st.session_state:
            del st.session_state["user_skills"]
        st.session_state.active_page = "results"
        st.rerun()

    # -- Career Results --
    results_disabled = not show_results
    results_label = "▶ Career Results" if (show_results and st.session_state.active_page == "results") else "○ Career Results"
    if show_results:
        results_label = "📊 Career Results"
    if st.button(results_label, key="nav_results", use_container_width=True, disabled=results_disabled):
        st.session_state.active_page = "results"
        st.rerun()

    # -- AI Chat --
    chat_disabled = not show_results
    chat_label = "💬 Career Advisor Chat" if show_results else "○ Career Advisor Chat"
    if st.button(chat_label, key="nav_chat", use_container_width=True, disabled=chat_disabled):
        st.session_state.active_page = "chat"
        st.rerun()

    st.divider()

    # ── Session Management ─────────────────────────────────────────────────────
    st.markdown("### Sessions")

    # Save current session (only relevant when there are results)
    if has_matches:
        with st.expander("💾 Save Session"):
            save_name = st.text_input(
                "Your name",
                placeholder="Enter your name",
                key="sidebar_save_name",
                label_visibility="collapsed"
            )
            if st.button("Save Results", type="primary", key="sidebar_save_btn", use_container_width=True):
                if save_name.strip():
                    success = save_session(save_name.strip())
                    if success:
                        st.success("Saved!")
                    else:
                        st.error("Save failed.")
                else:
                    st.warning("Enter a name first.")

    # Load a past session
    sessions = get_all_sessions()
    if sessions:
        with st.expander("📂 Load Session"):
            options = {
                f"{s['name']} · {s['date'][:10]} · {s['top_career']}": s["filename"]
                for s in sessions
            }
            selected = st.selectbox(
                "Pick a session",
                ["— select —"] + list(options.keys()),
                key="sidebar_session_select",
                label_visibility="collapsed"
            )
            if selected != "— select —":
                if st.button("Load →", type="primary", key="sidebar_load_btn", use_container_width=True):
                    data = load_session(options[selected])
                    if data:
                        restore_session(data)
                        st.session_state.active_page = "results"
                        st.success("Session loaded!")
                        st.rerun()
                    else:
                        st.error("Could not load.")

    st.divider()

    # ── Reset ──
    if quiz_started or has_matches:
        if st.button("🔄 Start Over", key="sidebar_reset", use_container_width=True):
            keys_to_clear = [
                "quiz_started", "current_question", "answers",
                "quiz_complete", "profile", "career_matches",
                "show_results", "explanations", "user_skills",
                "skill_checklist", "chat_history", "active_page"
            ]
            for key in keys_to_clear:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()


# ── Main Content Area ──────────────────────────────────────────────────────────
#
# The sidebar sets st.session_state.active_page.
# This block reads it and renders the correct page.
# State guards ensure users can't skip steps.
#
active_page = st.session_state.get("active_page", "results")

# Re-read flags after sidebar interactions
has_matches  = bool(st.session_state.get("career_matches"))
has_skills   = "user_skills" in st.session_state
show_results = st.session_state.get("show_results", False)

if show_results:
    # ── Results or Chat ──
    if active_page == "chat":
        render_chat()
    else:
        render_results()

elif has_matches and not has_skills:
    # ── Skills Assessment ──
    render_skills_assessment()

else:
    # ── Quiz / Landing ──
    if not st.session_state.get("quiz_started"):
        st.markdown("## Welcome to Career Guidance System")
        st.markdown(
            "Answer 8 short questions and discover the careers best matched "
            "to your interests, strengths, and values."
        )
        st.divider()
    render_quiz()
