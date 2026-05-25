# core/cv_analyzer.py

import urllib.parse
from ai.gemini_client import ask_gemini


def extract_text_from_pdf(uploaded_file) -> str:
    from pypdf import PdfReader
    import io

    pdf_bytes = io.BytesIO(uploaded_file.read())
    reader = PdfReader(pdf_bytes)

    full_text = ""
    for page in reader.pages:
        full_text += page.extract_text() + "\n"

    return full_text


def extract_skills_from_cv(cv_text: str, career: str) -> list:

    prompt = f"""
Extract all skills from this CV. Include:
- Programming languages (Python, Java, etc.)
- Frameworks and libraries (TensorFlow, React, etc.)
- Tools and platforms (Git, Docker, etc.)
- Technical concepts (Machine Learning, Algorithms, etc.)
- Soft skills (Leadership, Communication, etc.)

CV content:
{cv_text[:3000]}

Reply ONLY as a bullet list, one skill per line:
- skill name

List every skill you find, up to 15.
"""

    response = ask_gemini(prompt)

    if response.startswith("ERROR:"):
        return []

    return parse_skills_list(response)


def generate_skill_checklist(career: str) -> list:

    CAREER_SKILLS = {
        "Software Engineer": [
            "Python or Java programming",
            "Data structures & algorithms",
            "Version control (Git)",
            "Web development basics",
            "Database knowledge (SQL)",
            "Problem solving",
            "Object-oriented programming",
            "Testing & debugging",
            "API development",
            "Linux/command line"
        ],
        "Data Scientist": [
            "Python programming",
            "Machine learning",
            "Statistics & mathematics",
            "Data visualization",
            "SQL & databases",
            "Pandas & NumPy",
            "Deep learning basics",
            "Data cleaning",
            "Communication of insights",
            "Jupyter notebooks"
        ],
        "UX/UI Designer": [
            "Figma or Adobe XD",
            "User research",
            "Wireframing",
            "Prototyping",
            "Visual design principles",
            "Usability testing",
            "HTML/CSS basics",
            "Accessibility standards",
            "Design thinking",
            "Responsive design"
        ],
        "Product Manager": [
            "Product roadmapping",
            "User story writing",
            "Data analysis",
            "Stakeholder communication",
            "Agile & Scrum",
            "Market research",
            "Prioritization frameworks",
            "SQL basics",
            "Project management",
            "Presentation skills"
        ],
        "Cybersecurity Analyst": [
            "Network fundamentals",
            "Security tools (Wireshark, etc.)",
            "Linux operating system",
            "Threat analysis",
            "Cryptography basics",
            "Incident response",
            "Vulnerability scanning",
            "Python scripting",
            "Firewalls & IDS",
            "Security certifications (CompTIA)"
        ],
        "Business Analyst": [
            "Requirements gathering",
            "Data analysis",
            "SQL basics",
            "Process modeling",
            "Excel & spreadsheets",
            "Stakeholder management",
            "Documentation writing",
            "Presentation skills",
            "Problem solving",
            "Agile methodology"
        ],
        "Doctor / Medical Professional": [
            "Medical knowledge",
            "Clinical diagnosis",
            "Patient communication",
            "Medical terminology",
            "Critical thinking",
            "Research skills",
            "Teamwork",
            "Attention to detail",
            "Empathy",
            "Time management"
        ],
        "Psychologist / Counselor": [
            "Active listening",
            "Empathy & compassion",
            "Psychological theory",
            "Assessment techniques",
            "Communication skills",
            "Research methods",
            "Case documentation",
            "Ethical practice",
            "Cultural sensitivity",
            "Crisis intervention"
        ],
        "Mechanical Engineer": [
            "CAD software (AutoCAD/SolidWorks)",
            "Engineering mathematics",
            "Thermodynamics",
            "Materials science",
            "Technical drawing",
            "Problem solving",
            "Project management",
            "Programming basics",
            "Fluid mechanics",
            "Manufacturing processes"
        ],
        "Content Creator / Writer": [
            "Writing & storytelling",
            "SEO knowledge",
            "Social media platforms",
            "Video editing basics",
            "Audience research",
            "Content strategy",
            "Graphic design basics",
            "Analytics tools",
            "Consistency & scheduling",
            "Brand voice development"
        ]
    }

    if career in CAREER_SKILLS:
        return CAREER_SKILLS[career]

    prompt = f"""
List the 10 most important skills needed to become a {career}.

Reply ONLY as a bullet list:
- skill name

Keep each skill short and practical.
"""
    response = ask_gemini(prompt)

    if response.startswith("ERROR:"):
        return [
            "Communication skills",
            "Problem solving",
            "Domain knowledge",
            "Teamwork",
            "Continuous learning"
        ]

    return parse_skills_list(response)


def parse_skills_list(response: str) -> list:
    skills = []
    for line in response.strip().split("\n"):
        line = line.strip()
        if line.startswith("-") or line.startswith("*"):
            skill = line.lstrip("-* ").strip()
            if skill:
                skills.append(skill)
    return skills