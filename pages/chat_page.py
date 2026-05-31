# ui/pages/chat_page.py

import streamlit as st
from ai.gemini_client import ask_gemini
from ai.prompts import build_chat_system_prompt


def render_chat():
    """
    AI Chat interface — context-aware conversation
    using the user's profile and career results.
    """

    st.markdown("## 💬 Career Advisor Chat")
    st.caption("Ask anything about your results, career path, or next steps.")
    st.divider()

    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Build context from user's session
    profile     = st.session_state.get("profile", {})
    matches     = st.session_state.get("career_matches", [])
    user_skills = st.session_state.get("user_skills", [])

    # ── Display conversation history ──────────────────────────────────────────
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # ── Show suggested questions only if chat is empty ────────────────────────
    if not st.session_state.chat_history:
        render_suggested_questions()

    # ── Handle pending response from a suggested question click ───────────────
    #
    # WHY THIS EXISTS:
    # When a user clicks a suggested question, we add it to chat_history
    # and set pending_response = True, then rerun.
    # On the next render, this block catches it and generates the AI reply.
    # Without this, the AI reply only triggers when the user types something.
    #
    if st.session_state.get("pending_response"):
        st.session_state.pending_response = False   # clear the flag immediately

        last_message = st.session_state.chat_history[-1]

        # Safety check — only process if the last message is from the user
        if last_message["role"] == "user":
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = generate_response(
                        last_message["content"],
                        st.session_state.chat_history,
                        profile,
                        matches,
                        user_skills
                    )
                st.markdown(response)

            st.session_state.chat_history.append({
                "role":    "assistant",
                "content": response
            })
            st.rerun()

    # ── Handle typed messages ─────────────────────────────────────────────────
    user_input = st.chat_input("Ask your career advisor anything...")

    if user_input:
        # Add user message to history
        st.session_state.chat_history.append({
            "role":    "user",
            "content": user_input
        })

        # Show user message immediately
        with st.chat_message("user"):
            st.markdown(user_input)

        # Generate and show AI response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = generate_response(
                    user_input,
                    st.session_state.chat_history,
                    profile,
                    matches,
                    user_skills
                )
            st.markdown(response)

        # Add AI response to history
        st.session_state.chat_history.append({
            "role":    "assistant",
            "content": response
        })

        st.rerun()


def generate_response(
    user_input: str,
    history: list,
    profile: dict,
    matches: list,
    user_skills: list
) -> str:
    """
    Sends the full conversation + user context to the AI
    and returns a response.
    """

    system_prompt = build_chat_system_prompt(profile, matches, user_skills)

    # Build conversation history as readable text
    # We exclude the last message since it's the current question
    history_text = ""
    for msg in history[:-1]:
        role = "Student" if msg["role"] == "user" else "Advisor"
        history_text += f"{role}: {msg['content']}\n"

    full_prompt = f"""
{system_prompt}

CONVERSATION SO FAR:
{history_text}

Student: {user_input}

Advisor:"""

    return ask_gemini(full_prompt)


def render_suggested_questions():
    """
    Shows clickable starter questions when chat history is empty.
    
    HOW IT WORKS:
    Clicking a question → adds it to chat_history + sets pending_response flag
    → st.rerun() → render_chat() detects the flag → generates AI reply
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
        col = cols[i % 2]
        with col:
            if st.button(question, key=f"suggested_{i}"):
                # Add the question as a user message
                st.session_state.chat_history.append({
                    "role":    "user",
                    "content": question
                })
                # Signal that we need an AI response on the next render
                st.session_state.pending_response = True
                st.rerun()
