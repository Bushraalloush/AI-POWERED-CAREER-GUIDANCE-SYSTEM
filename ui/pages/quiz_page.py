# ui/pages/quiz_page.py

import streamlit as st
from core.quiz_engine import get_all_questions, get_total_questions


def initialize_quiz():
    if "quiz_started" not in st.session_state:
        st.session_state.quiz_started = False
    if "current_question" not in st.session_state:
        st.session_state.current_question = 0
    if "answers" not in st.session_state:
        st.session_state.answers = {}
    if "quiz_complete" not in st.session_state:
        st.session_state.quiz_complete = False


def render_quiz():
    initialize_quiz()

    questions = get_all_questions()
    total     = get_total_questions()

    if not st.session_state.quiz_started:
        render_welcome_screen()
    elif not st.session_state.quiz_complete:
        render_question(questions, total)
    else:
        render_completion_screen()


def render_welcome_screen():
    st.markdown("## Career Discovery Assessment")
    st.markdown("""
    This assessment takes approximately 3 minutes and covers four key areas:

    - Your interests and what excites you professionally
    - Your strengths and areas of natural ability
    - Your preferred work environment and pace
    - What you value most in a long-term career
    """)

    st.info("Answer honestly. There are no right or wrong answers — the more accurate your responses, the better your career matches will be.")

    if st.button("Begin Assessment", type="primary"):
        st.session_state.quiz_started = True
        st.rerun()


def render_question(questions, total):
    current_index = st.session_state.current_question
    question_data = questions[current_index]

    progress = current_index / total
    st.progress(progress)
    st.caption(f"Question {current_index + 1} of {total}")

    st.markdown("---")
    st.markdown(f"### {question_data['question']}")

    selected = st.radio(
        label="Select one answer:",
        options=question_data["options"],
        index=None,
        key=f"q_{current_index}"
    )

    st.markdown("---")

    col1, col2 = st.columns([3, 1])

    with col2:
        if st.button("Continue", type="primary", disabled=selected is None):
            st.session_state.answers[question_data["key"]] = {
                "question": question_data["question"],
                "answer":   selected,
                "dimension": question_data["dimension"]
            }

            if current_index + 1 >= total:
                st.session_state.quiz_complete = True
            else:
                st.session_state.current_question += 1

            st.rerun()


def render_completion_screen():
    from core.profiler import build_profile
    from core.career_matcher import match_careers

    st.success("Assessment complete.")
    st.markdown("### Analyzing your profile...")

    if "profile" not in st.session_state:
        with st.spinner("Building your career profile..."):
            st.session_state.profile = build_profile(
                st.session_state.answers
            )

    if "career_matches" not in st.session_state:
        with st.spinner("Matching you to careers..."):
            st.session_state.career_matches = match_careers(
                st.session_state.profile
            )

    if not st.session_state.career_matches:
        st.error("The AI service is temporarily unavailable. Please wait a moment and try again.")
        if st.button("Try Again"):
            del st.session_state["career_matches"]
            st.rerun()
        return

    st.rerun()