# 🎯 AI-Powered Career Guidance System

> From 8 honest answers to a personalized career roadmap — built with Python, Streamlit, and LLMs.

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.45+-FF4B4B?style=flat&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Groq](https://img.shields.io/badge/Groq-Llama_3.3_70B-F55036?style=flat)](https://groq.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat)](LICENSE)

---

## 📌 Overview

Most career quizzes ask *"do you prefer data or people?"* and call it guidance.
This project does something different.

The **AI Career Guidance System** is a full-stack web application that takes a structured 8-question assessment and produces a deeply personalized career analysis — powered by a real large language model. It scores career paths across four dimensions, identifies your skill gaps, generates a learning roadmap, and lets you continue the conversation with an AI advisor that already knows your full profile.

Built as a solo graduation capstone project in 4 weeks.

**[🚀 Live Demo →](https://your-app.streamlit.app)** <!-- Replace with your Streamlit Cloud URL -->

---

## ✨ Features

### 6-Stage User Journey

| Stage | What Happens |
|-------|-------------|
| **1. Quiz** | 8 questions covering interests, technical skills, work style, and career values |
| **2. Profile** | Answers are structured into a 4-dimension profile used by every downstream module |
| **3. Skills Intake** | Upload your CV (PDF) or manually select skills from a checklist |
| **4. AI Matching** | LLM scores 10 career paths against your profile across 4 sub-dimensions |
| **5. Results Dashboard** | Full exploration: salary, trends, skill gaps, roadmap, resources, interview prep |
| **6. AI Chat** | Context-aware career advisor — it already knows you before you type a word |

### Results Dashboard — What's Inside Each Match

- 📊 **Salary Insights** — Entry / Mid / Senior ranges + top hiring companies
- 📈 **Market Trend** — Growth direction, demand level, automation risk, 5-year outlook
- 💡 **Why It Fits** — Personalized explanation tied to your specific profile
- 🔍 **Skill Gap Analysis** — Skills you have vs. skills to develop
- 🗺️ **Learning Roadmap** — 4-phase plan: Foundation → Core → Specialization → Job-Ready
- 📚 **Learning Resources** — Courses, books, practice platforms, communities
- 🎤 **Interview Prep** — 5 tailored questions with answering tips
- ❌ **Careers to Avoid** — Bottom matches explained honestly

### Other Capabilities

- **CV Upload** — PDF parsing via `pypdf`, skills extracted by the LLM
- **Session Save / Load** — Save results by name, reload any previous session
- **Dual-Provider AI Failover** — Groq as primary, Cerebras as automatic fallback
- **AI Response Caching** — Results cached in session state, no repeated API calls
- **Dark Navy UI** — Custom CSS matching a professional dark theme

---

## 🏗️ Architecture

```
app.py                        ← Entry point, routing, navigation, progress bar
│
├── ui/
│   ├── pages/
│   │   ├── quiz_page.py      ← 8-question assessment flow
│   │   ├── skills_page.py    ← CV upload + manual checklist
│   │   ├── results_page.py   ← Full results dashboard
│   │   ├── chat_page.py      ← Context-aware AI chat
│   │   └── roadmap_page.py   ← 4-phase learning roadmap
│   └── components/
│       └── styles.py         ← Custom CSS injection
│
├── core/
│   ├── quiz_engine.py        ← Question bank (8 questions, 4 dimensions)
│   ├── profiler.py           ← Builds structured profile from answers
│   ├── career_matcher.py     ← LLM career scoring + response parsing
│   ├── skill_analyzer.py     ← Skill gap analysis
│   ├── roadmap_generator.py  ← 4-phase roadmap generation
│   ├── salary_insights.py    ← Salary range + company data
│   ├── career_trend.py       ← Market trend analysis
│   ├── interview_prep.py     ← Interview question generation
│   ├── resource_recommender.py ← Courses, books, communities
│   └── cv_analyzer.py        ← PDF extraction + skill parsing
│
├── ai/
│   ├── gemini_client.py      ← Groq + Cerebras dual-provider client
│   └── prompts.py            ← Chat system prompt builder
│
├── sessions/
│   ├── session_manager.py    ← Save / load / restore sessions (JSON)
│   └── data/                 ← Saved session files
│
├── config/
│   └── settings.py           ← API key loading (.env + st.secrets)
│
├── .streamlit/
│   └── config.toml           ← Dark theme configuration
│
└── requirements.txt
```

**Design principle:** Each module has a single responsibility. Every feature is a clean function call — adding a new feature means adding one module and one UI call, nothing else breaks.

---

## 🤖 How the AI Matching Works

The user profile is sent to the LLM with a carefully structured prompt that asks it to act as a career evaluator. The model returns data in a strict format:

```
Software Engineer: 87 | 90 | 85 | 88 | 82
                  ↑      ↑    ↑    ↑    ↑
               overall  int  skills style values
```

This is parsed line by line, converted to tuples, and sorted by overall score. No fuzzy text parsing — the prompt enforces a format the parser can reliably extract numbers from.

If Groq hits a rate limit, `ask_gemini()` automatically retries via Cerebras with the same model (`llama3.3-70b`) and the same messages — zero changes required downstream. The function name `ask_gemini` is a legacy artifact from early development kept for backwards compatibility.

---

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- A [Groq API key](https://console.groq.com) (free)
- A [Cerebras API key](https://cloud.cerebras.ai) (free, optional but recommended as fallback)

### 1. Clone the repository

```bash
git clone https://github.com/your-username/ai-career-guidance.git
cd ai-career-guidance
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up API keys

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
CEREBRAS_API_KEY=your_cerebras_api_key_here
```

### 4. Run the app

```bash
streamlit run app.py
```

The app opens at `http://localhost:8501`

---

## ☁️ Deploying to Streamlit Cloud

1. Push the project to a public GitHub repository
2. Go to [share.streamlit.io](https://share.streamlit.io) and connect your repo
3. Set `app.py` as the entry point
4. Add your secrets under **Settings → Secrets**:

```toml
GROQ_API_KEY = "your_groq_api_key_here"
CEREBRAS_API_KEY = "your_cerebras_api_key_here"
```

The app reads secrets from both `.env` (local) and `st.secrets` (cloud) automatically.

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Frontend | Streamlit + Custom CSS | Web UI, navigation, dark theme |
| AI Primary | Groq — Llama 3.3 70B | Career matching, all AI generation |
| AI Fallback | Cerebras — Llama 3.3 70B | Automatic failover on rate limits |
| PDF Parsing | pypdf | CV text extraction |
| Session Storage | JSON files | Save/load user sessions |
| Secrets | python-dotenv + st.secrets | Local and cloud key management |
| Deployment | Streamlit Community Cloud | Live hosting |

---

## 📁 Project Structure Notes

**Why Streamlit?**
Pure Python web UI with no JavaScript, no routing config, no templates. The right call for a solo 4-week build. Custom CSS via `st.markdown()` handles theming.

**Why JSON for sessions?**
Intentional MVP choice. No database setup overhead. Sessions are human-readable, easy to inspect, and trivial to restore. A real production version would use a proper database with authentication.

**Why two AI providers?**
Groq is fast and has a generous free tier but can rate-limit under load. Cerebras provides instant failover with zero code changes downstream — the abstraction in `ask_gemini()` means no other file ever needs to know which provider responded.

---

## ⚠️ Known Limitations

- **Salary data** is LLM-generated, not pulled from a live API — treat as directional reference only
- **10 career paths** are hardcoded — the architecture supports expansion via the `CAREERS` list in `career_matcher.py`
- **No authentication** — sessions are identified by name only
- **Parser fragility** — if the LLM returns a malformed line, it's silently skipped; users may occasionally see "Not available"

---

## 🔮 Future Improvements

- [ ] Real-time job market data via Bureau of Labor Statistics or LinkedIn API
- [ ] Expand from 10 to 100+ dynamic career paths (database-driven)
- [ ] User authentication and persistent session history
- [ ] ML-powered matching trained on labeled user data
- [ ] Arabic language support (MENA region focus)
- [ ] Anonymous analytics dashboard for institutions

---

## 👩‍💻 Author

**Bushra**
Computer Science — Graduation Capstone Project
Built solo over 4 weeks · June 2026

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

> *"Career guidance should be personal, practical, and accessible. That's what this project tries to be."*
