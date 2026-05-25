# ui/pages/skills_page.py

import streamlit as st
from core.cv_analyzer import (
    extract_text_from_pdf,
    extract_skills_from_cv,
    generate_skill_checklist
)


def render_skills_assessment():

    top_career = st.session_state.career_matches[0][0]

    st.markdown("## Skills Assessment")
    st.markdown(f"Let's identify what skills you already have for **{top_career}** and where the gaps are.")
    st.divider()

    method = st.radio(
        "How would you like to provide your skills?",
        options=["Upload CV", "Fill manually"],
        horizontal=True
    )

    st.markdown("---")

    if method == "Upload CV":
        render_cv_upload(top_career)
    else:
        render_manual_checklist(top_career)

    st.markdown("---")

    # Back button
    if st.button("← Back to Quiz"):
        keys_to_clear = [
            "quiz_started", "current_question", "answers",
            "quiz_complete", "career_matches", "profile",
            "skill_checklist"
        ]
        for key in keys_to_clear:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()


def render_cv_upload(career: str):

    st.markdown("### Upload Your CV")
    st.caption("PDF format only. Your CV is processed locally and never stored.")

    uploaded_file = st.file_uploader(
        "Select your CV file",
        type=["pdf"]
    )

    if uploaded_file:
        with st.spinner("Reading your CV..."):
            cv_text = extract_text_from_pdf(uploaded_file)

        if not cv_text.strip():
            st.error("Could not read this PDF. Please try the manual option instead.")
            return

        st.success("CV read successfully.")

        with st.spinner("Extracting skills from your CV..."):
            extracted_skills = extract_skills_from_cv(cv_text, career)

        if not extracted_skills:
            st.warning("No skills could be extracted. Please use the manual option.")
            return

        st.markdown(f"### {len(extracted_skills)} skills found in your CV")
        st.caption("Uncheck any skills you do not actually have.")

        confirmed = []
        for skill in extracted_skills:
            if st.checkbox(skill, value=True, key=f"cv_{skill}"):
                confirmed.append(skill)

        st.markdown("---")

        if st.button(
            "Continue to Results",
            type="primary",
            disabled=len(confirmed) == 0
        ):
            st.session_state.user_skills = confirmed
            st.session_state.show_results = True
            st.rerun()


def render_manual_checklist(career: str):

    st.markdown("### Skills Checklist")
    st.caption(f"Select every skill you are comfortable with for {career}.")

    if "skill_checklist" not in st.session_state:
        with st.spinner("Loading skills checklist..."):
            st.session_state.skill_checklist = generate_skill_checklist(career)

    checklist = st.session_state.skill_checklist

    if not checklist:
        st.error("Could not load the skills list. Please refresh the page.")
        return

    selected = []
    for skill in checklist:
        if st.checkbox(skill, key=f"manual_{skill}"):
            selected.append(skill)

    st.markdown("---")
    st.caption(f"{len(selected)} of {len(checklist)} skills selected")

    if st.button("Continue to Results", type="primary"):
        st.session_state.user_skills = selected
        st.session_state.show_results = True
        st.rerun()