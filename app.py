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

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:

    # App identity
    st.markdown("## 🎯 Career Guidance")
    st.caption("AI-powered career discovery platform")
    st.divider()

    # ── AI Provider Status ──
    provider = get_current_provider()
    if provider != "None":
        st.markdown(f"**AI Engine** &nbsp; `{provider}`", unsafe_allow_html=True)
    else:
        st.markdown("**AI Engine** &nbsp; `Offline`", unsafe_allow_html=True)

    st.divider()

    # ── Progress / State indicators ──
    has_matches  = bool(st.session_state.get("career_matches"))
    has_skills   = "user_skills" in st.session_state
    show_results = st.session_state.get("show_results", False)
    quiz_started = st.session_state.get("quiz_started", False)
    quiz_done    = st.session_state.get("quiz_complete", False)

    st.markdown("### Navigation")

    # Step indicators — show user where they are
    def nav_item(icon, label, active=False, done=False):
        if done:
            color = "#10B981"   # green
            status = "✓"
        elif active:
            color = "#2563EB"   # blue
            status = "→"
        else:
            color = "#475569"   # grey
            status = "○"

        st.markdown(
            f"<div style='padding:6px 0; color:{color}; font-size:0.9rem;'>"
            f"{status} {icon} {label}</div>",
            unsafe_allow_html=True
        )

    nav_item("📋", "Career Quiz",
             active=quiz_started and not quiz_done,
             done=quiz_done)

    nav_item("🛠️", "Skills Assessment",
             active=has_matches and not has_skills,
             done=has_skills)

    nav_item("📊", "Career Results",
             active=show_results and not (has_matches and not has_skills),
             done=show_results)

    nav_item("💬", "AI Career Advisor",
             active=show_results,
             done=False)

    st.divider()

    # ── Session Management ──
    st.markdown("### Sessions")

    # Save current session
    if has_matches:
        with st.expander("💾 Save Session"):
            save_name = st.text_input(
                "Your name",
                placeholder="Enter your name",
                key="sidebar_save_name"
            )
            if st.button("Save", type="primary", key="sidebar_save_btn"):
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
                f"{s['name']} — {s['date'][:10]}": s["filename"]
                for s in sessions
            }
            selected = st.selectbox(
                "Pick a session",
                ["— select —"] + list(options.keys()),
                key="sidebar_session_select",
                label_visibility="collapsed"
            )
            if selected != "— select —":
                if st.button("Load", type="primary", key="sidebar_load_btn"):
                    data = load_session(options[selected])
                    if data:
                        restore_session(data)
                        st.success("Loaded!")
                        st.rerun()
                    else:
                        st.error("Could not load.")

    st.divider()

    # ── Reset ──
    if quiz_started or has_matches:
        if st.button("🔄 Start Over", key="sidebar_reset"):
            keys_to_clear = [
                "quiz_started", "current_question", "answers",
                "quiz_complete", "profile", "career_matches",
                "show_results", "explanations", "user_skills",
                "skill_checklist", "chat_history", "pending_response"
            ]
            for key in keys_to_clear:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()

    # ── Footer ──
    st.markdown(
        "<div style='position:absolute; bottom:1.5rem; left:0; right:0;"
        "text-align:center; color:#334155; font-size:0.75rem;'>"
        "Career Guidance System v1.0</div>",
        unsafe_allow_html=True
    )


# ── Main Content Area ──────────────────────────────────────────────────────────

has_matches  = bool(st.session_state.get("career_matches"))
has_skills   = "user_skills" in st.session_state
show_results = st.session_state.get("show_results", False)

# ── Results + Chat ─────────────────────────────────────────────────────────────
if show_results:
    tab1, tab2 = st.tabs(["📊 Career Results", "💬 Career Advisor Chat"])
    with tab1:
        render_results()
    with tab2:
        render_chat()

# ── Skills Assessment ──────────────────────────────────────────────────────────
elif has_matches and not has_skills:
    render_skills_assessment()

# ── Quiz / Landing ─────────────────────────────────────────────────────────────
else:
    # Welcome header — only shown on the landing/quiz screen
    st.markdown("## Welcome to Career Guidance System")
    st.markdown(
        "Answer 8 short questions and discover the careers best matched "
        "to your interests, strengths, and values."
    )
    st.divider()
    render_quiz()
