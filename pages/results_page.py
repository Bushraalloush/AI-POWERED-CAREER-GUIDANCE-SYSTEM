# ui/pages/results_page.py

import streamlit as st
from ai.gemini_client import ask_gemini
from core.profiler import format_profile_for_ai
from core.skill_analyzer import analyze_skill_gap
from core.resource_recommender import get_resources_for_skills, build_search_url
from core.salary_insights import get_salary_insights
from core.career_trend import get_career_trend
from core.interview_prep import get_interview_questions
from ui.pages.roadmap_page import render_roadmap


def render_results():

    matches = st.session_state.career_matches
    profile = st.session_state.profile

    if "explanations" not in st.session_state:
        st.session_state.explanations = {}

    st.markdown("## Career Match Results")
    st.markdown("Based on your assessment, here are your top career matches ranked by compatibility.")

    if st.button("← Back to Skills Assessment"):
        keys_to_clear = [
            "show_results", "user_skills",
            "skill_checklist", "explanations"
        ]
        for key in keys_to_clear:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()

    st.divider()

    top_matches = matches[:5]

    for i, match in enumerate(top_matches):

        if len(match) == 3:
            career, score, dimensions = match
        else:
            career, score = match
            dimensions = {}

        if score >= 80:
            indicator = "Strong Match"
        elif score >= 60:
            indicator = "Good Match"
        else:
            indicator = "Partial Match"

        with st.expander(
            f"#{i+1} — {career}  |  {score}% — {indicator}",
            expanded=(i == 0)
        ):
            st.progress(score / 100)

            # --- Score Breakdown ---
            if dimensions:
                render_score_breakdown(dimensions)

            # --- Salary Insights ---
            salary_key = f"salary_{career}"

            if salary_key in st.session_state:
                render_salary(st.session_state[salary_key])
            else:
                if st.button(
                    "View Salary Insights",
                    key=f"salary_{i}"
                ):
                    with st.spinner("Loading salary data..."):
                        salary = get_salary_insights(career)
                    st.session_state[salary_key] = salary
                    st.rerun()

            # --- Career Trend ---
            st.markdown("---")
            trend_key = f"trend_{career}"

            if trend_key in st.session_state:
                render_trend(st.session_state[trend_key])
            else:
                if st.button(
                    "View Market Trend",
                    key=f"trend_{i}"
                ):
                    with st.spinner("Analyzing market trend..."):
                        trend = get_career_trend(career)
                    st.session_state[trend_key] = trend
                    st.rerun()

            # --- Why This Career Suits Me ---
            st.markdown("---")

            if career in st.session_state.explanations:
                st.markdown(st.session_state.explanations[career])
            else:
                if st.button(
                    "Why this career suits me",
                    key=f"explain_{i}"
                ):
                    with st.spinner("Generating explanation..."):
                        explanation = get_career_explanation(
                            career, score, profile
                        )
                    st.session_state.explanations[career] = explanation
                    st.rerun()

            # --- Skill Gap ---
            st.markdown("---")
            skill_key = f"skills_{career}"

            if skill_key in st.session_state:
                render_skill_gap(st.session_state[skill_key])
            else:
                if st.button(
                    "Analyze skill gap",
                    key=f"gap_{i}"
                ):
                    with st.spinner("Analyzing skill gap..."):
                        gap = analyze_skill_gap(
                            career,
                            st.session_state.get("user_skills", [])
                        )
                    st.session_state[skill_key] = gap
                    st.rerun()

            # --- Learning Roadmap ---
            st.markdown("---")
            roadmap_key = f"show_roadmap_{career}"

            if st.button(
                "View Learning Roadmap",
                key=f"roadmap_{i}"
            ):
                st.session_state[roadmap_key] = True
                st.rerun()

            if st.session_state.get(roadmap_key):
                gap_data = st.session_state.get(
                    f"skills_{career}", {"missing": []}
                )
                render_roadmap(career, gap_data["missing"])

            # --- Learning Resources ---
            st.markdown("---")
            resources_key = f"resources_{career}"

            if resources_key in st.session_state:
                render_resources(st.session_state[resources_key])
            else:
                if st.button(
                    "Get Learning Resources",
                    key=f"resources_{i}"
                ):
                    gap_data = st.session_state.get(
                        f"skills_{career}", {"missing": []}
                    )
                    with st.spinner("Finding the best resources..."):
                        resources = get_resources_for_skills(
                            career,
                            gap_data["missing"]
                        )
                    st.session_state[resources_key] = resources
                    st.rerun()

            # --- Interview Prep ---
            st.markdown("---")
            interview_key = f"interview_{career}"

            if interview_key in st.session_state:
                render_interview_prep(
                    st.session_state[interview_key], career
                )
            else:
                if st.button(
                    "Prepare for Interview",
                    key=f"interview_{i}"
                ):
                    with st.spinner("Generating interview questions..."):
                        questions = get_interview_questions(
                            career,
                            st.session_state.get("user_skills", [])
                        )
                    st.session_state[interview_key] = questions
                    st.rerun()

    # --- Careers to Avoid ---
    st.divider()
    render_careers_to_avoid(matches, profile)

    st.divider()

    if st.button("Retake Assessment"):
        keys_to_clear = [
            "quiz_started", "current_question", "answers",
            "quiz_complete", "profile", "career_matches",
            "show_results", "explanations", "user_skills",
            "skill_checklist"
        ]
        for key in keys_to_clear:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()


def render_careers_to_avoid(matches: list, profile: dict):
    """Shows bottom 3 career matches with honest explanations."""

    st.markdown("### Careers That May Not Suit You")
    st.caption(
        "These careers scored lowest based on your profile. "
        "This is not a judgment — it helps you focus your energy wisely."
    )

    # Get bottom 3 matches
    bottom_matches = matches[-3:][::-1]

    profile_text = format_profile_for_ai(profile)

    for match in bottom_matches:
        if len(match) == 3:
            career, score, _ = match
        else:
            career, score = match

        avoid_key = f"avoid_{career}"

        with st.expander(f"{career}  |  {score}% Match"):
            st.progress(score / 100)

            if avoid_key in st.session_state:
                st.warning(st.session_state[avoid_key])
            else:
                if st.button(
                    "Why this may not suit me",
                    key=f"avoid_btn_{career}"
                ):
                    with st.spinner("Analyzing..."):
                        explanation = get_avoid_explanation(
                            career, score, profile_text
                        )
                    st.session_state[avoid_key] = explanation
                    st.rerun()


def get_avoid_explanation(career: str, score: int, profile_text: str) -> str:

    prompt = f"""
You are an honest career counselor.

This user scored only {score}% for: {career}

{profile_text}

In 2-3 sentences, explain specifically why this career
is likely a poor fit based on their profile.

Be honest but respectful. Focus on mismatches between
their profile and what the career demands.
Do not be discouraging about their overall potential.
"""
    return ask_gemini(prompt)


def render_score_breakdown(dimensions: dict):

    st.markdown("**Score Breakdown**")

    labels = {
        "interests":  "Interests",
        "skills":     "Skills",
        "work_style": "Work Style",
        "values":     "Values"
    }

    col1, col2 = st.columns(2)
    items = list(dimensions.items())
    half  = len(items) // 2

    with col1:
        for key, val in items[:half]:
            label = labels.get(key, key)
            st.caption(f"{label}: {val}%")
            st.progress(val / 100)

    with col2:
        for key, val in items[half:]:
            label = labels.get(key, key)
            st.caption(f"{label}: {val}%")
            st.progress(val / 100)

    st.markdown("---")


def render_salary(salary: dict):

    st.markdown("### Salary Insights")
    st.caption(
        "AI-estimated ranges based on global market data. "
        "Actual salaries vary by country, company, and experience. "
        "Use as a general reference only."
    )

    def clean(text):
        return text.replace("$", "USD ").replace("`", "")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("**Entry Level**")
        st.write(clean(salary["entry"]))

    with col2:
        st.markdown("**Mid Level**")
        st.write(clean(salary["mid"]))

    with col3:
        st.markdown("**Senior Level**")
        st.write(clean(salary["senior"]))

    if salary["companies"]:
        st.markdown("---")
        st.markdown("**Top Hiring Companies:**")
        companies = "  •  ".join(salary["companies"])
        st.write(companies)

    if salary["notes"]:
        st.info(salary["notes"])


def render_trend(trend: dict):

    st.markdown("### Market Trend")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("**Direction**")
        st.write(trend.get("direction", "Unknown"))

    with col2:
        st.markdown("**Market Demand**")
        st.write(trend.get("demand", "Unknown"))

    with col3:
        st.markdown("**Automation Risk**")
        st.write(trend.get("automation_risk", "Unknown"))

    if trend.get("outlook"):
        st.info(trend["outlook"])

    if trend.get("driver"):
        st.caption(f"Key Driver: {trend['driver']}")


def render_day_in_life(day: dict, career: str):

    st.markdown(f"### A Day as a {career}")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("**Morning**")
        st.write(day.get("morning", ""))

    with col2:
        st.markdown("**Afternoon**")
        st.write(day.get("afternoon", ""))

    with col3:
        st.markdown("**Evening**")
        st.write(day.get("evening", ""))

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        if day.get("environment"):
            st.markdown("**Work Environment**")
            st.write(day["environment"])

        if day.get("tools"):
            st.markdown("**Tools Used Daily**")
            st.write(day["tools"])

    with col2:
        if day.get("best_part"):
            st.success(day["best_part"])

        if day.get("hardest_part"):
            st.warning(day["hardest_part"])


def render_interview_prep(questions: list, career: str):

    st.markdown(f"### Interview Preparation — {career}")
    st.caption("Practice these likely questions before your interview.")

    if not questions:
        st.warning("Could not generate questions. Please try again.")
        return

    for j, q in enumerate(questions):
        with st.expander(f"Q{j+1}: {q.get('question', '')}"):
            if q.get("tip"):
                st.info(f"Tip: {q['tip']}")


def get_career_explanation(career: str, score: int, profile: dict) -> str:

    profile_text = format_profile_for_ai(profile)

    prompt = f"""
You are a career guidance counselor. Be concise and specific.

User scored {score}% match for: {career}

{profile_text}

Reply in exactly this format — 3 bullet points per section, no paragraphs:

WHY IT FITS:
- Point about their interests
- Point about their strengths
- Point about their work style or values

WHAT YOU WILL DO:
- Day to day task 1
- Day to day task 2
- Day to day task 3

KEY CHALLENGE:
- The main challenge and how to overcome it

Be direct and specific. Reference their actual profile. No filler phrases.
"""
    return ask_gemini(prompt)


def render_skill_gap(gap: dict):

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Skills You Have**")
        for skill in gap["existing"]:
            st.success(f"{skill}")

    with col2:
        st.markdown("**Skills to Develop**")
        for skill in gap["missing"]:
            st.warning(f"{skill}")


def render_resources(resources: dict):

    st.markdown("### Learning Resources")

    tab1, tab2, tab3, tab4 = st.tabs([
        "Online Courses",
        "Books",
        "Practice",
        "Communities"
    ])

    with tab1:
        st.caption("Pricing and availability may vary. Click to verify before enrolling.")
        items = resources.get("free_courses", [])
        if items:
            for item in items:
                parts = item.split("|")
                if len(parts) >= 2:
                    name     = parts[0].strip()
                    platform = parts[1].strip()
                    url      = build_search_url(f"{name} {platform}")
                    st.markdown(f"**{name}**")
                    st.caption(f"Platform: {platform}")
                    st.markdown(f"[Search for this course]({url})")
                    st.markdown("---")
        else:
            st.caption("No courses found.")

    with tab2:
        items = resources.get("books", [])
        if items:
            for item in items:
                parts = item.split("|")
                if len(parts) >= 2:
                    title  = parts[0].strip()
                    author = parts[1].strip()
                    url    = build_search_url(f"{title} {author} book")
                    st.markdown(f"**{title}**")
                    st.caption(f"by {author}")
                    st.markdown(f"[Search for this book]({url})")
                    st.markdown("---")
        else:
            st.caption("No books found.")

    with tab3:
        items = resources.get("practice_platforms", [])
        if items:
            for item in items:
                parts = item.split("|")
                if len(parts) >= 2:
                    platform = parts[0].strip()
                    action   = parts[1].strip()
                    url      = build_search_url(platform)
                    st.markdown(f"**{platform}**")
                    st.caption(action)
                    st.markdown(f"[Visit {platform}]({url})")
                    st.markdown("---")
        else:
            st.caption("No platforms found.")

    with tab4:
        items = resources.get("communities", [])
        if items:
            for item in items:
                parts = item.split("|")
                if len(parts) >= 2:
                    name  = parts[0].strip()
                    where = parts[1].strip()
                    url   = build_search_url(f"{name} {where} community")
                    st.markdown(f"**{name}**")
                    st.caption(f"Find it on: {where}")
                    st.markdown(f"[Find this community]({url})")
                    st.markdown("---")
        else:
            st.caption("No communities found.")