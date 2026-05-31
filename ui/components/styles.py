# ui/components/styles.py

import streamlit as st


def apply_custom_styles():
    st.markdown("""
    <style>

    /* ── Google Font ── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* ── Global ── */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* ── Hide Streamlit Branding — SURGICAL: only hide branding, NOT the header ──
       Why: hiding `header` entirely also hides the sidebar toggle button.
       Instead we hide only the toolbar (deploy button, menu) and decoration bar.
    ── */
    #MainMenu                        { visibility: hidden; }
    footer                           { visibility: hidden; }
    [data-testid="stToolbar"]        { display: none !important; }
    [data-testid="stDecoration"]     { display: none !important; }
    [data-testid="stStatusWidget"]   { display: none !important; }

    /* Make header transparent so it takes no visual space,
       but the sidebar toggle button inside it stays clickable */
    [data-testid="stHeader"] {
        background-color: transparent !important;
        border-bottom: none !important;
    }

    /* ── Main Container ── */
    .main .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        max-width: 900px;
        margin: 0 auto;
    }

    /* ── App Title ── */
    h1 {
        font-size: 2rem !important;
        font-weight: 700 !important;
        color: #F1F5F9 !important;
        letter-spacing: -0.5px;
        margin-bottom: 0 !important;
    }

    /* ── Section Headings ── */
    h2 {
        font-size: 1.4rem !important;
        font-weight: 600 !important;
        color: #F1F5F9 !important;
        margin-top: 1.5rem !important;
    }

    h3 {
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        color: #CBD5E1 !important;
    }

    /* ── Body Text ── */
    p, li, label {
        font-size: 0.95rem !important;
        color: #94A3B8 !important;
        line-height: 1.6 !important;
    }

    /* ── Caption Text ── */
    .stCaption, small {
        color: #64748B !important;
        font-size: 0.8rem !important;
    }

    /* ── Primary Button ── */
    .stButton > button[kind="primary"] {
        background-color: #2563EB !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.5rem 1.5rem !important;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
        transition: background-color 0.2s ease !important;
    }

    .stButton > button[kind="primary"]:hover {
        background-color: #1D4ED8 !important;
    }

    /* ── Secondary Button ── */
    .stButton > button {
        background-color: #1E293B !important;
        color: #CBD5E1 !important;
        border: 1px solid #334155 !important;
        border-radius: 8px !important;
        font-size: 0.9rem !important;
        transition: all 0.2s ease !important;
    }

    .stButton > button:hover {
        border-color: #2563EB !important;
        color: #F1F5F9 !important;
    }

    /* ── Expander ── */
    .streamlit-expanderHeader {
        background-color: #1E293B !important;
        border: 1px solid #334155 !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        color: #F1F5F9 !important;
        padding: 0.8rem 1rem !important;
    }

    .streamlit-expanderContent {
        background-color: #1E293B !important;
        border: 1px solid #334155 !important;
        border-top: none !important;
        border-radius: 0 0 10px 10px !important;
        padding: 1rem !important;
    }

    /* ── Progress Bar ── */
    .stProgress > div > div {
        background-color: #2563EB !important;
        border-radius: 4px !important;
    }

    .stProgress > div {
        background-color: #1E293B !important;
        border-radius: 4px !important;
    }

    /* ── Alert Boxes ── */
    .stSuccess {
        background-color: #064E3B !important;
        border: 1px solid #10B981 !important;
        border-radius: 8px !important;
        color: #D1FAE5 !important;
    }

    .stWarning {
        background-color: #78350F !important;
        border: 1px solid #F59E0B !important;
        border-radius: 8px !important;
        color: #FEF3C7 !important;
    }

    .stInfo {
        background-color: #1E3A5F !important;
        border: 1px solid #2563EB !important;
        border-radius: 8px !important;
        color: #DBEAFE !important;
    }

    .stError {
        background-color: #450A0A !important;
        border: 1px solid #EF4444 !important;
        border-radius: 8px !important;
        color: #FEE2E2 !important;
    }

    /* ── Radio Buttons ── */
    .stRadio > label {
        color: #CBD5E1 !important;
        font-weight: 500 !important;
    }

    /* ── Divider ── */
    hr {
        border-color: #1E293B !important;
        margin: 1.5rem 0 !important;
    }

    /* ── File Uploader ── */
    .stFileUploader {
        background-color: #1E293B !important;
        border: 1px dashed #334155 !important;
        border-radius: 10px !important;
        padding: 1rem !important;
    }

    /* ── Input Fields ── */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background-color: #1E293B !important;
        border: 1px solid #334155 !important;
        border-radius: 8px !important;
        color: #F1F5F9 !important;
        font-size: 0.95rem !important;
    }

    /* ═══════════════════════════════════════
       SIDEBAR
    ═══════════════════════════════════════ */

    [data-testid="stSidebar"] {
        background-color: #080E1A !important;
        border-right: 1px solid #1E293B !important;
        min-width: 260px !important;
        max-width: 260px !important;
    }

    /* Sidebar title */
    [data-testid="stSidebar"] h2 {
        font-size: 1.1rem !important;
        color: #F1F5F9 !important;
        margin-top: 0 !important;
        margin-bottom: 0 !important;
    }

    /* Sidebar section label (h3) */
    [data-testid="stSidebar"] h3 {
        font-size: 0.7rem !important;
        font-weight: 700 !important;
        color: #334155 !important;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-top: 0.25rem !important;
        margin-bottom: 0.1rem !important;
    }

    /* Sidebar generic text */
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] label {
        color: #64748B !important;
        font-size: 0.82rem !important;
    }

    /* Sidebar caption */
    [data-testid="stSidebar"] .stCaption {
        color: #475569 !important;
        font-size: 0.78rem !important;
    }

    /* ── Sidebar buttons (nav items) ── */
    [data-testid="stSidebar"] .stButton > button {
        width: 100% !important;
        text-align: left !important;
        background-color: transparent !important;
        border: none !important;
        border-radius: 6px !important;
        color: #94A3B8 !important;
        font-size: 0.88rem !important;
        font-weight: 400 !important;
        padding: 0.45rem 0.75rem !important;
        margin-bottom: 2px !important;
        transition: all 0.15s ease !important;
    }

    [data-testid="stSidebar"] .stButton > button:hover {
        background-color: #1E293B !important;
        color: #F1F5F9 !important;
        border: none !important;
    }

    /* Sidebar primary buttons (Save, Load) */
    [data-testid="stSidebar"] .stButton > button[kind="primary"] {
        background-color: #2563EB !important;
        color: #FFFFFF !important;
        border: none !important;
        font-weight: 500 !important;
        text-align: center !important;
        padding: 0.45rem 0.75rem !important;
    }

    [data-testid="stSidebar"] .stButton > button[kind="primary"]:hover {
        background-color: #1D4ED8 !important;
    }

    /* Sidebar disabled buttons */
    [data-testid="stSidebar"] .stButton > button:disabled {
        color: #1E293B !important;
        cursor: not-allowed !important;
    }

    /* ── Sidebar expanders ── */
    [data-testid="stSidebar"] .streamlit-expanderHeader {
        font-size: 0.85rem !important;
        font-weight: 500 !important;
        padding: 0.45rem 0.6rem !important;
        background-color: #0F1929 !important;
        border: 1px solid #1E293B !important;
        color: #94A3B8 !important;
        border-radius: 6px !important;
    }

    [data-testid="stSidebar"] .streamlit-expanderContent {
        background-color: #080E1A !important;
        border: 1px solid #1E293B !important;
        border-top: none !important;
        padding: 0.5rem 0.6rem !important;
        border-radius: 0 0 6px 6px !important;
    }

    /* ── Sidebar selectbox ── */
    [data-testid="stSidebar"] .stSelectbox > div > div {
        background-color: #0F1929 !important;
        border-color: #1E293B !important;
        color: #CBD5E1 !important;
        font-size: 0.82rem !important;
    }

    /* ── Sidebar text input ── */
    [data-testid="stSidebar"] .stTextInput > div > div > input {
        background-color: #0F1929 !important;
        border-color: #1E293B !important;
        color: #F1F5F9 !important;
        font-size: 0.85rem !important;
    }

    /* ── Sidebar divider ── */
    [data-testid="stSidebar"] hr {
        border-color: #1E293B !important;
        margin: 0.6rem 0 !important;
    }

    /* ── Tabs ── */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #1E293B !important;
        border-radius: 8px !important;
        padding: 4px !important;
        gap: 4px !important;
    }

    .stTabs [data-baseweb="tab"] {
        color: #94A3B8 !important;
        font-weight: 500 !important;
        border-radius: 6px !important;
        font-size: 0.9rem !important;
    }

    .stTabs [aria-selected="true"] {
        background-color: #2563EB !important;
        color: #FFFFFF !important;
    }

    /* ── Chat Messages ── */
    [data-testid="stChatMessage"] {
        background-color: #1E293B !important;
        border: 1px solid #334155 !important;
        border-radius: 10px !important;
        padding: 0.8rem !important;
        margin-bottom: 0.5rem !important;
    }

    /* ── Chat Input ── */
    [data-testid="stChatInput"] {
        background-color: #1E293B !important;
        border: 1px solid #334155 !important;
        border-radius: 10px !important;
    }

    [data-testid="stChatInput"] textarea {
        color: #F1F5F9 !important;
        font-size: 0.9rem !important;
    }

    </style>
    """, unsafe_allow_html=True)
