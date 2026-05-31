# ui/pages/chat_page.py

import streamlit as st
from ai.gemini_client import ask_chat
from ai.prompts import build_chat_system_prompt


def render_chat():
    """
    AI Chat interface — context-aware conversation
    using the user's profile and career results.
    """

    st.markdown("## Career Advisor Chat")
    st.caption("Ask anything about your results, career path, or next steps.")
    st.divider()

    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Build context from user's session
    profile     = st.session_state.get("profile", {})
    matches     = st.session_state.get("career_matches", [])
    user_skills = st.session_state.get("user_skills", [])

    # Build the system prompt once — it doesn't change during the session
    system_prompt = build_chat_system_prompt(profile, matches, user_skills)

    # Display full conversation history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Show suggested starter questions when chat is empty
    if not st.session_state.chat_history:
        render_suggested_questions()

    # Chat input field
    user_input = st.chat_input("Ask your career advisor anything...")

    if user_input:
        # Add user message to history and display it immediately
        st.session_state.chat_history.append({
            "role":    "user",
            "content": user_input
        })

        with st.chat_message("user"):
            st.markdown(user_input)

        # Generate and display AI response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = generate_response(
                    user_input,
                    st.session_state.chat_history,
                    system_prompt
                )

            if response.startswith("ERROR:"):
                # Show a red error box — do NOT save errors to chat history
                # Also remove the user message we just added so they can retry cleanly
                st.error(response.replace("ERROR:", "").strip())
                st.session_state.chat_history.pop()
            else:
                st.markdown(response)
                # Only save valid AI responses to history
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

    WHY this is better than the old single-string approach:
    - Old approach: crammed system prompt + history + new message into ONE user message string
    - New approach: system context in 'system' role, history as alternating user/assistant turns,
      new question as the final user message
    - LLMs are trained specifically on this format — response quality and consistency
      improve significantly when context is sent in the correct roles
    """

    # Start with the system prompt in the dedicated system role
    messages = [
        {"role": "system", "content": system_prompt}
    ]

    # Add conversation history as proper alternating turns.
    # We exclude the last entry in history because that's the current user_input
    # we just appended — it would appear twice if we included it here.
    for msg in history[:-1]:
        messages.append({
            "role":    msg["role"],      # "user" or "assistant"
            "content": msg["content"]
        })

    # Add the current user question as the final turn
    messages.append({
        "role":    "user",
        "content": user_input
    })

    return ask_chat(messages)


def render_suggested_questions():
    """Shows clickable starter questions when the chat history is empty."""

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
                st.session_state.chat_history.append({
                    "role":    "user",
                    "content": question
                })
                st.rerun()