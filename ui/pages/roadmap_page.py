# ui/pages/roadmap_page.py

import streamlit as st
from core.roadmap_generator import generate_roadmap


def render_roadmap(career: str, missing_skills: list):
    """
    Displays the learning roadmap for the target career.
    Called from results_page when user requests it.
    """

    st.markdown("---")
    st.markdown("### Learning Roadmap")
    st.caption(f"A step-by-step plan to become a {career}.")

    # Cache so it doesn't regenerate on every click
    roadmap_key = f"roadmap_{career}"

    if roadmap_key not in st.session_state:
        with st.spinner("Building your personalized roadmap..."):
            st.session_state[roadmap_key] = generate_roadmap(
                career, missing_skills
            )

    phases = st.session_state[roadmap_key]

    if not phases:
        st.error("Could not generate roadmap. Please try again.")
        if st.button("Retry", key=f"retry_roadmap_{career}"):
            del st.session_state[roadmap_key]
            st.rerun()
        return

    # Display each phase as a clean card
    for i, phase in enumerate(phases):
        render_phase_card(phase, i)


def render_phase_card(phase: dict, index: int):
    """Renders a single roadmap phase."""

    phase_labels = ["Foundation", "Core Development",
                    "Specialization", "Job Readiness"]

    label = phase_labels[index] if index < len(phase_labels) else f"Phase {index + 1}"

    with st.expander(
        f"Phase {index + 1} — {label}  |  {phase['duration']}",
        expanded=(index == 0)
    ):
        if phase["goal"]:
            st.info(phase["goal"])

        st.markdown("**Action Steps:**")
        for step in phase["steps"]:
            st.markdown(f"- {step}")