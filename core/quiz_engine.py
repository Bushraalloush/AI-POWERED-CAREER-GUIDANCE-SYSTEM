# core/quiz_engine.py

# Each question has:
# - "question": what the user sees
# - "options": list of choices
# - "dimension": which profile category this feeds into
# - "key": short unique name for this question

QUIZ_QUESTIONS = [
    {
        "key": "work_preference",
        "dimension": "interests",
        "question": "Which of these sounds most like your ideal work?",
        "options": [
            "Building or fixing things (software, machines, systems)",
            "Helping and communicating with people",
            "Analyzing data and solving complex problems",
            "Creating content, designs, or artistic work",
            "Leading teams and making strategic decisions"
        ]
    },
    {
        "key": "subject_passion",
        "dimension": "interests",
        "question": "Which subject or field excites you the most?",
        "options": [
            "Technology and computers",
            "Science and medicine",
            "Business and economics",
            "Arts and humanities",
            "Social sciences and psychology"
        ]
    },
    {
        "key": "tech_comfort",
        "dimension": "skills",
        "question": "How comfortable are you with technology and programming?",
        "options": [
            "Very comfortable — I enjoy coding or technical work",
            "Comfortable — I can use tools and learn quickly",
            "Neutral — I can manage but it's not my strength",
            "Prefer non-technical work"
        ]
    },
    {
        "key": "strength",
        "dimension": "skills",
        "question": "What do people most often praise you for?",
        "options": [
            "Problem-solving and logical thinking",
            "Communication and leadership",
            "Creativity and original ideas",
            "Attention to detail and organization",
            "Empathy and understanding people"
        ]
    },
    {
        "key": "work_style",
        "dimension": "work_style",
        "question": "Which work environment fits you best?",
        "options": [
            "Quiet and independent — I focus best alone",
            "Collaborative — I thrive working with a team",
            "Dynamic — I like variety and switching tasks",
            "Structured — I prefer clear processes and routines"
        ]
    },
    {
        "key": "work_style_pace",
        "dimension": "work_style",
        "question": "How do you handle pressure and deadlines?",
        "options": [
            "I perform well under pressure — it motivates me",
            "I prefer steady, predictable workloads",
            "I like some challenge but not constant urgency",
            "I work best with flexible timelines"
        ]
    },
    {
        "key": "core_value",
        "dimension": "values",
        "question": "What matters most to you in a career?",
        "options": [
            "High salary and financial growth",
            "Making a positive impact on society",
            "Creative freedom and self-expression",
            "Job stability and security",
            "Continuous learning and growth"
        ]
    },
    {
        "key": "work_impact",
        "dimension": "values",
        "question": "How do you want your work to affect the world?",
        "options": [
            "Build technology that improves lives",
            "Help individuals directly through services",
            "Influence business or economic systems",
            "Create culture through art or media",
            "Advance scientific or academic knowledge"
        ]
    }
]


def get_all_questions():
    """Return the full list of quiz questions."""
    return QUIZ_QUESTIONS


def get_total_questions():
    """Return how many questions are in the quiz."""
    return len(QUIZ_QUESTIONS)