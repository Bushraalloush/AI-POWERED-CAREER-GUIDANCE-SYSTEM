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

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Career Guidance System",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

apply_custom_styles()


# ══════════════════════════════════════════════════════════════════════════════
# PROGRESS CALCULATION
# One single function that reads session_state and returns the correct
# progress float (0.0 → 1.0), a label, and the current step number.
#
# WHY here and not inside a page:
#   Streamlit only renders code that actually executes in a given run.
#   If progress logic lived inside quiz_page.py, it would vanish the
#   moment routing sends the user to a different page.
#   Putting it in app.py guarantees it runs on EVERY rerun.
# ══════════════════════════════════════════════════════════════════════════════

def get_app_progress() -> tuple:
    """
    Returns (progress_float, step_label, current_step, total_steps).
    Reads only from st.session_state — safe across reruns.
    """
    total_steps  = 4
    quiz_started  = st.session_state.get("quiz_started", False)
    quiz_complete = st.session_state.get("quiz_complete", False)
    has_skills    = "user_skills" in st.session_state
    show_results  = st.session_state.get("show_results", False)

    if not quiz_started:
        return 0.0, "Step 1 of 4 — Start the assessment", 0, total_steps

    elif quiz_started and not quiz_complete:
        # Give fine-grained progress WITHIN the quiz step (0% → 25%)
        current_q  = st.session_state.get("current_question", 0)
        total_q    = 8
        q_fraction = current_q / total_q          # 0.0 → 1.0 within this step
        progress   = round(q_fraction * 0.25, 3)  # maps to 0.00 → 0.25
        return progress, f"Step 1 of 4 — Question {current_q + 1} of {total_q}", 1, total_steps

    elif quiz_complete and not has_skills:
        return 0.50, "Step 2 of 4 — Skills assessment", 2, total_steps

    elif has_skills and not show_results:
        return 0.75, "Step 3 of 4 — Viewing your results", 3, total_steps

    else:
        return 1.0, "Step 4 of 4 — Complete ✓", 4, total_steps


# ══════════════════════════════════════════════════════════════════════════════
# NAVIGATION
# WHY a top navigation bar instead of sidebar:
#   - initial_sidebar_state="collapsed" hides the sidebar by default.
#     A sidebar nav would be invisible until the user manually opens it.
#   - Top nav using st.tabs() or buttons in st.columns() always renders.
#   - Navigation must live in app.py so it runs unconditionally every rerun.
#
# Navigation here is informational + jump-capable (where state allows).
# We can't freely jump to any page — the app needs quiz data to show results.
# So we show all steps but only enable the ones the user has unlocked.
# ══════════════════════════════════════════════════════════════════════════════

def render_top_nav():
    """
    Renders the top navigation bar.
    Shows all steps. Highlights the current step.
    Only shows jump buttons for unlocked steps so state stays consistent.
    """
    quiz_started  = st.session_state.get("quiz_started", False)
    quiz_complete = st.session_state.get("quiz_complete", False)
    has_skills    = "user_skills" in st.session_state
    show_results  = st.session_state.get("show_results", False)

    # Determine current page name for highlighting
    if not quiz_started:
        current_page = "Welcome"
    elif quiz_started and not quiz_complete:
        current_page = "Quiz"
    elif quiz_complete and not has_skills:
        current_page = "Skills"
    elif has_skills and not show_results:
        current_page = "Results"
    else:
        current_page = "Results"

    nav_col1, nav_col2, nav_col3, nav_col4, nav_col5 = st.columns([1, 1, 1, 1, 1])

    # Step 1 — Quiz (always accessible, resets to start)
    with nav_col1:
        label = "🟣 **Quiz**" if current_page in ("Welcome", "Quiz") else "⚪ Quiz"
        if st.button(label, key="nav_quiz", use_container_width=True):
            # Clear everything and go back to quiz start
            keys = [
                "quiz_started", "current_question", "answers", "quiz_complete",
                "profile", "career_matches", "show_results", "user_skills",
                "skill_checklist", "explanations", "chat_history"
            ]
            for k in keys:
                st.session_state.pop(k, None)
            st.rerun()

    # Step 2 — Skills (only if quiz is done)
    with nav_col2:
        if quiz_complete:
            label = "🟣 **Skills**" if current_page == "Skills" else "⚪ Skills"
            if st.button(label, key="nav_skills", use_container_width=True):
                # Go back to skills page
                st.session_state.pop("user_skills", None)
                st.session_state.pop("show_results", None)
                st.session_state.pop("skill_checklist", None)
                st.rerun()
        else:
            st.button("🔒 Skills", key="nav_skills_locked",
                      disabled=True, use_container_width=True)

    # Step 3 — Results (only if skills done)
    with nav_col3:
        if has_skills:
            label = "🟣 **Results**" if current_page == "Results" and not show_results else "⚪ Results"
            # show_results flag is what triggers the results page
            if st.button(label, key="nav_results", use_container_width=True):
                st.session_state["show_results"] = True
                st.rerun()
        else:
            st.button("🔒 Results", key="nav_results_locked",
                      disabled=True, use_container_width=True)

    # Step 4 — Chat (only if results unlocked)
    with nav_col4:
        if show_results:
            label = "🟣 **Chat**" if current_page == "Chat" else "⚪ Chat"
            if st.button(label, key="nav_chat", use_container_width=True):
                st.session_state["show_results"] = True
                st.session_state["nav_tab"] = "chat"
                st.rerun()
        else:
            st.button("🔒 Chat", key="nav_chat_locked",
                      disabled=True, use_container_width=True)

    # Step 5 — Restart
    with nav_col5:
        if st.button("🔄 Restart", key="nav_restart", use_container_width=True):
            st.session_state.clear()
            st.rerun()

    st.markdown("---")


# ══════════════════════════════════════════════════════════════════════════════
# HEADER — runs on every rerun
# ══════════════════════════════════════════════════════════════════════════════

st.markdown("## 🎯 Career Guidance System")
st.caption("Discover the career path built for your strengths and goals.")

provider = get_current_provider()
if provider and provider != "None":
    st.caption(f"AI Provider: {provider}")

# ── Progress bar — ONE place, always correct ───────────────────────────────
progress_val, progress_label, current_step, total_steps = get_app_progress()
st.progress(progress_val)
st.caption(progress_label)

st.markdown("---")

# ── Navigation bar — runs unconditionally on every rerun ──────────────────
render_top_nav()


# ══════════════════════════════════════════════════════════════════════════════
# ROUTING
# Simple state-driven routing. The navigation bar above handles user-initiated
# page changes by updating session_state then calling st.rerun().
# ══════════════════════════════════════════════════════════════════════════════

has_matches  = bool(st.session_state.get("career_matches"))
has_skills   = "user_skills" in st.session_state
show_results = st.session_state.get("show_results", False)

# ── Results page ──────────────────────────────────────────────────────────
if show_results:

    # Save session widget
    st.markdown("### 💾 Save Your Results")
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
                    st.success("Saved successfully.")
                else:
                    st.error("Save failed. Check terminal.")
            else:
                st.warning("Enter your name first.")

    st.divider()

    # Tabs — check if nav requested the chat tab directly
    default_tab = st.session_state.pop("nav_tab", "results")
    tab1, tab2 = st.tabs(["📊 Results", "💬 Career Advisor Chat"])
    with tab1:
        render_results()
    with tab2:
        render_chat()

# ── Skills assessment ─────────────────────────────────────────────────────
elif has_matches and not has_skills:
    render_skills_assessment()

# ── Quiz / Welcome ────────────────────────────────────────────────────────
else:
    # Load previous session panel — only before quiz starts
    sessions = get_all_sessions()

    if sessions and not st.session_state.get("quiz_started"):
        st.markdown("### 📂 Load a Previous Session")

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
