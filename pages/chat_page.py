# ui/pages/chat_page.py

import streamlit as st
from ai.gemini_client import ask_chat
from ai.prompts import build_chat_system_prompt


def render_chat():
    """
    AI Chat interface — context-aware conversation
    using the user's profile and career results.

    BUG #3 FIX — Suggested questions now auto-generate responses.

    ROOT CAUSE OF OLD BUG:
        The old suggested question buttons did:
            1. Append question to chat_history
            2. Call st.rerun()
        On rerun, render_chat() ran again. The message appeared in
        the history display. But the AI response code only lives
        inside "if user_input:" where user_input = st.chat_input().
        st.chat_input() returns None on a rerun triggered by a button
        click (not a real chat submission). So the "if user_input:"
        block NEVER ran and no AI response was ever generated.

    THE FIX:
        Instead of appending + rerunning, the button sets:
            st.session_state.pending_question = question
        Then calls st.rerun().
        At the TOP of render_chat() we check for pending_question.
        If it exists we pop it, generate the AI response, save both
        messages to history, then rerun to display cleanly.
    """

    st.markdown("## Career Advisor Chat")
    st.caption("Ask anything about your results, career path, or next steps.")
    st.divider()

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    profile     = st.session_state.get("profile", {})
    matches     = st.session_state.get("career_matches", [])
    user_skills = st.session_state.get("user_skills", [])

    system_prompt = build_chat_system_prompt(profile, matches, user_skills)

    # ── PENDING QUESTION HANDLER ───────────────────────────────────────────
    # MUST run before any widget is rendered.
    # WHY: if this ran after st.chat_input(), widget order would differ
    # between reruns causing a DuplicateWidgetID error in Streamlit.
    pending = st.session_state.pop("pending_question", None)

    if pending:
        st.session_state.chat_history.append({
            "role":    "user",
            "content": pending
        })

        with st.spinner("Thinking..."):
            response = generate_response(
                pending,
                st.session_state.chat_history,
                system_prompt
            )

        if response.startswith("ERROR:"):
            st.session_state.chat_history.pop()
            st.error(response.replace("ERROR:", "").strip())
        else:
            st.session_state.chat_history.append({
                "role":    "assistant",
                "content": response
            })

        st.rerun()

    # ── DISPLAY CONVERSATION HISTORY ──────────────────────────────────────
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # ── SUGGESTED QUESTIONS (only when chat is empty) ─────────────────────
    if not st.session_state.chat_history:
        render_suggested_questions()

    # ── LIVE CHAT INPUT ───────────────────────────────────────────────────
    user_input = st.chat_input("Ask your career advisor anything...")

    if user_input:
        st.session_state.chat_history.append({
            "role":    "user",
            "content": user_input
        })

        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = generate_response(
                    user_input,
                    st.session_state.chat_history,
                    system_prompt
                )

            if response.startswith("ERROR:"):
                st.error(response.replace("ERROR:", "").strip())
                st.session_state.chat_history.pop()
            else:
                st.markdown(response)
                st.session_state.chat_history.append({
                    "role":    "assistant",
                    "content": response
                })

        st.rerun()


def generate_response(
    user_input: str,
    history: list,
    system_prompt: str,
) -> str:
    """
    Builds a properly structured messages list and sends it to the AI.
    System prompt in the system role, history as alternating turns,
    current question as the final user message.
    """
    messages = [{"role": "system", "content": system_prompt}]

    for msg in history[:-1]:
        messages.append({"role": msg["role"], "content": msg["content"]})

    messages.append({"role": "user", "content": user_input})

    return ask_chat(messages)


def render_suggested_questions():
    """
    Renders clickable starter questions.

    FIX: Buttons set pending_question flag instead of directly appending
    to chat_history. This lets render_chat() handle both the append AND
    the AI response generation on the next rerun, before any widgets render.
    """
    st.markdown("**Not sure where to start? Try one of these:**")

    questions = [
        "Which of my top careers should I focus on?",
        "How long will it take me to be job-ready?",
        "What should I learn first given my current skills?",
        "Am I a good fit for a technical career?",
        "What salary can I expect in my top career match?"
    ]

    cols = st.columns(2)

    for i, question in enumerate(questions):
        with cols[i % 2]:
            if st.button(question, key=f"suggested_{i}", use_container_width=True):
                st.session_state.pending_question = question
                st.rerun()
