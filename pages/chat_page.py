# ui/pages/chat_page.py

import streamlit as st
from ai.gemini_client import ask_gemini
from ai.prompts import build_chat_system_prompt


def render_chat():
    """
    AI Chat interface — context-aware conversation
    using the user's profile and career results.

    ARCHITECTURE NOTE — how message flow works:
    ─────────────────────────────────────────────
    All messages (typed OR from suggested buttons) follow ONE path:

      1. Message is appended to chat_history as role="user"
      2. st.rerun() is called
      3. On re-render, we display all messages from history
      4. We check: is the last message from the user with no reply yet?
         If YES → generate AI response, append it, rerun again
         If NO  → do nothing, just show the chat input

    This eliminates the need for flags and handles both inputs uniformly.
    """

    st.markdown("## 💬 Career Advisor Chat")
    st.caption("Ask anything about your results, career path, or next steps.")
    st.divider()

    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Pull context from session
    profile     = st.session_state.get("profile", {})
    matches     = st.session_state.get("career_matches", [])
    user_skills = st.session_state.get("user_skills", [])

    # ── Step 1: Display all messages in history ───────────────────────────────
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # ── Step 2: Show suggested questions if chat is empty ────────────────────
    if not st.session_state.chat_history:
        render_suggested_questions()

    # ── Step 3: Unified response generator ───────────────────────────────────
    #
    # Check if the last message in history is from the user.
    # If it is, that means no AI response exists yet — generate one.
    # This handles BOTH suggested question clicks AND typed messages.
    #
    needs_response = (
        len(st.session_state.chat_history) > 0
        and st.session_state.chat_history[-1]["role"] == "user"
    )

    if needs_response:
        last_user_message = st.session_state.chat_history[-1]["content"]

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = generate_response(
                    last_user_message,
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
        return  # stop here — rerun will re-enter this function cleanly

    # ── Step 4: Chat input for new typed messages ─────────────────────────────
    user_input = st.chat_input("Ask your career advisor anything...")

    if user_input:
        # Just add to history and rerun.
        # Step 3 above will detect the pending user message and respond.
        st.session_state.chat_history.append({
            "role":    "user",
            "content": user_input
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
    Builds the full prompt (system context + conversation history + new message)
    and returns the AI response.
    """

    system_prompt = build_chat_system_prompt(profile, matches, user_skills)

    # Build conversation history as readable text.
    # We exclude the last message (the current user question)
    # since it's passed separately as user_input.
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
    Shows clickable starter questions when the chat is empty.

    HOW IT WORKS:
    Clicking a button appends the question to chat_history as a user message,
    then calls st.rerun(). On the next render, the unified response generator
    in render_chat() detects that the last message is from the user and
    automatically generates the AI reply — no flags needed.
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
            if st.button(question, key=f"suggested_{i}", use_container_width=True):
                st.session_state.chat_history.append({
                    "role":    "user",
                    "content": question
                })
                # No flag needed — just rerun.
                # render_chat() will detect the pending user message on re-entry.
                st.rerun()
