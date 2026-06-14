import re
import time

import plotly.graph_objects as go
import streamlit as st

from agents.ats_agent import get_ats_report
from agents.github_agent import get_github_projects
from agents.portfolio_agent import get_portfolio_skills
from agents.resume_agent import build_resume
from utils.latex_generator import generate_latex
from utils.parser import read_resume
from utils.pdf_generator import generate_pdf

# ─────────────────────────────────────────────────────────────────────────────
# Page config
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ResumeForge AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# Session state defaults
# ─────────────────────────────────────────────────────────────────────────────
_DEFAULTS = {
    "generated_resume": None,
    "ats_report": None,
    "github_data": [],
    "portfolio_data": "",
    "resume_text": "",
    "ats_score": None,
    "step": 1,
    "last_build_time": None,
}
for _key, _val in _DEFAULTS.items():
    if _key not in st.session_state:
        st.session_state[_key] = _val

# ─────────────────────────────────────────────────────────────────────────────
# Custom CSS — premium dark glassmorphism theme
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

    :root {
        --bg-primary: #0a0a0f;
        --bg-secondary: #12121a;
        --bg-card: rgba(255, 255, 255, 0.03);
        --border: rgba(255, 255, 255, 0.08);
        --accent: #6366f1;
        --accent-2: #8b5cf6;
        --accent-3: #06b6d4;
        --success: #10b981;
        --warning: #f59e0b;
        --danger: #ef4444;
        --text-primary: #f1f5f9;
        --text-muted: #94a3b8;
        --glow: 0 0 40px rgba(99, 102, 241, 0.15);
    }

    .stApp {
        background: var(--bg-primary);
        background-image:
            radial-gradient(ellipse 80% 60% at 10% -10%, rgba(99,102,241,0.18) 0%, transparent 60%),
            radial-gradient(ellipse 60% 50% at 90% 110%, rgba(139,92,246,0.12) 0%, transparent 60%),
            radial-gradient(ellipse 40% 30% at 50% 50%, rgba(6,182,212,0.05) 0%, transparent 70%);
        font-family: 'Inter', sans-serif;
    }

    #MainMenu, footer, header { visibility: hidden; }

    /* Hero */
    .hero {
        background: linear-gradient(135deg, rgba(99,102,241,0.12) 0%, rgba(139,92,246,0.08) 50%, rgba(6,182,212,0.06) 100%);
        border: 1px solid var(--border);
        border-radius: 20px;
        padding: 2.5rem 3rem;
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
        box-shadow: var(--glow);
    }
    .hero::before {
        content: '';
        position: absolute;
        top: -50%; right: -20%;
        width: 400px; height: 400px;
        background: radial-gradient(circle, rgba(99,102,241,0.1) 0%, transparent 70%);
        pointer-events: none;
    }
    .hero-badge {
        display: inline-block;
        background: rgba(99,102,241,0.2);
        border: 1px solid rgba(99,102,241,0.4);
        color: #a5b4fc;
        padding: 4px 14px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-bottom: 1rem;
    }
    .hero h1 {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #e2e8f0 0%, #a5b4fc 50%, #67e8f9 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0 0 0.75rem 0;
        line-height: 1.1;
    }
    .hero p {
        color: var(--text-muted);
        font-size: 1.05rem;
        margin: 0;
        max-width: 600px;
        line-height: 1.6;
    }

    /* Metric cards */
    .metric-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1rem;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 1.25rem 1.5rem;
        backdrop-filter: blur(12px);
        transition: border-color 0.2s, transform 0.2s;
    }
    .metric-card:hover {
        border-color: rgba(99,102,241,0.3);
        transform: translateY(-2px);
    }
    .metric-icon { font-size: 1.5rem; margin-bottom: 0.5rem; }
    .metric-value {
        font-size: 1.75rem;
        font-weight: 700;
        color: var(--text-primary);
        line-height: 1;
    }
    .metric-label {
        font-size: 0.78rem;
        color: var(--text-muted);
        margin-top: 0.35rem;
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }
    .metric-delta {
        font-size: 0.8rem;
        margin-top: 0.4rem;
        font-weight: 500;
    }
    .delta-up { color: var(--success); }
    .delta-neutral { color: var(--text-muted); }

    /* Feature cards */
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1rem;
        margin: 1.5rem 0 2rem 0;
    }
    .feature-card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 1.5rem;
        transition: all 0.25s ease;
    }
    .feature-card:hover {
        border-color: rgba(99,102,241,0.35);
        background: rgba(99,102,241,0.05);
        transform: translateY(-3px);
        box-shadow: 0 8px 32px rgba(99,102,241,0.1);
    }
    .feature-icon {
        width: 44px; height: 44px;
        background: linear-gradient(135deg, rgba(99,102,241,0.3), rgba(139,92,246,0.2));
        border-radius: 12px;
        display: flex; align-items: center; justify-content: center;
        font-size: 1.3rem;
        margin-bottom: 1rem;
    }
    .feature-title {
        font-size: 0.95rem;
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 0.4rem;
    }
    .feature-desc {
        font-size: 0.82rem;
        color: var(--text-muted);
        line-height: 1.5;
    }

    /* Step progress */
    .steps {
        display: flex;
        align-items: center;
        gap: 0;
        margin-bottom: 2rem;
        padding: 1.25rem 2rem;
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 16px;
    }
    .step {
        display: flex;
        align-items: center;
        gap: 0.6rem;
        flex: 1;
    }
    .step-num {
        width: 32px; height: 32px;
        border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-size: 0.8rem;
        font-weight: 700;
        border: 2px solid var(--border);
        color: var(--text-muted);
        flex-shrink: 0;
        transition: all 0.3s;
    }
    .step-num.active {
        background: linear-gradient(135deg, var(--accent), var(--accent-2));
        border-color: transparent;
        color: white;
        box-shadow: 0 0 20px rgba(99,102,241,0.4);
    }
    .step-num.done {
        background: rgba(16,185,129,0.2);
        border-color: var(--success);
        color: var(--success);
    }
    .step-label {
        font-size: 0.82rem;
        font-weight: 500;
        color: var(--text-muted);
    }
    .step-label.active { color: var(--text-primary); font-weight: 600; }
    .step-connector {
        flex: 1;
        height: 2px;
        background: var(--border);
        margin: 0 0.75rem;
        max-width: 60px;
    }
    .step-connector.done { background: var(--success); }

    /* Resume preview box */
    .resume-preview {
        background: #0d0d14;
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 2rem;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.82rem;
        line-height: 1.7;
        color: #cbd5e1;
        max-height: 500px;
        overflow-y: auto;
        white-space: pre-wrap;
        word-break: break-word;
    }
    .resume-preview::-webkit-scrollbar { width: 6px; }
    .resume-preview::-webkit-scrollbar-track { background: transparent; }
    .resume-preview::-webkit-scrollbar-thumb {
        background: rgba(99,102,241,0.4);
        border-radius: 3px;
    }

    /* ATS report box */
    .ats-box {
        background: linear-gradient(135deg, rgba(16,185,129,0.06), rgba(99,102,241,0.06));
        border: 1px solid rgba(16,185,129,0.2);
        border-radius: 16px;
        padding: 1.75rem;
        color: #cbd5e1;
        font-size: 0.9rem;
        line-height: 1.7;
        white-space: pre-wrap;
    }

    /* Status pills */
    .status-pill {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    .pill-ready { background: rgba(16,185,129,0.15); color: #34d399; border: 1px solid rgba(16,185,129,0.3); }
    .pill-pending { background: rgba(148,163,184,0.1); color: #94a3b8; border: 1px solid rgba(148,163,184,0.2); }
    .pill-active { background: rgba(99,102,241,0.15); color: #a5b4fc; border: 1px solid rgba(99,102,241,0.3); }

    /* Section headers */
    .section-header {
        font-size: 1.1rem;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .section-header::after {
        content: '';
        flex: 1;
        height: 1px;
        background: var(--border);
        margin-left: 0.5rem;
    }

    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background: var(--bg-secondary) !important;
        border-right: 1px solid var(--border);
    }
    section[data-testid="stSidebar"] .stMarkdown h2 {
        font-size: 0.75rem !important;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: var(--text-muted) !important;
    }

    /* Buttons */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        letter-spacing: 0.02em !important;
        transition: all 0.2s !important;
        box-shadow: 0 4px 20px rgba(99,102,241,0.3) !important;
    }
    .stButton > button[kind="primary"]:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 28px rgba(99,102,241,0.45) !important;
    }
    .stButton > button[kind="secondary"] {
        background: var(--bg-card) !important;
        border: 1px solid var(--border) !important;
        border-radius: 10px !important;
        color: var(--text-primary) !important;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 4px;
        gap: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px !important;
        color: var(--text-muted) !important;
        font-weight: 500 !important;
        font-size: 0.85rem !important;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, rgba(99,102,241,0.25), rgba(139,92,246,0.15)) !important;
        color: #a5b4fc !important;
    }

    /* Download buttons */
    .stDownloadButton > button {
        background: rgba(6,182,212,0.1) !important;
        border: 1px solid rgba(6,182,212,0.3) !important;
        color: #67e8f9 !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
    }

    /* File uploader */
    [data-testid="stFileUploader"] {
        border: 1px dashed rgba(99,102,241,0.3) !important;
        border-radius: 12px !important;
        background: rgba(99,102,241,0.03) !important;
    }

    /* Expander */
    .streamlit-expanderHeader {
        background: var(--bg-card) !important;
        border-radius: 10px !important;
        border: 1px solid var(--border) !important;
    }

    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem 0 1rem;
        color: var(--text-muted);
        font-size: 0.78rem;
        border-top: 1px solid var(--border);
        margin-top: 3rem;
    }

    /* GitHub project chips */
    .project-chip {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(99,102,241,0.1);
        border: 1px solid rgba(99,102,241,0.25);
        border-radius: 8px;
        padding: 6px 12px;
        margin: 4px;
        font-size: 0.8rem;
        color: #a5b4fc;
    }
    .lang-badge {
        background: rgba(6,182,212,0.15);
        color: #67e8f9;
        padding: 1px 7px;
        border-radius: 4px;
        font-size: 0.72rem;
    }

    @media (max-width: 900px) {
        .metric-grid { grid-template-columns: repeat(2, 1fr); }
        .feature-grid { grid-template-columns: 1fr; }
        .hero h1 { font-size: 2rem; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────
def _extract_ats_score(report: str) -> int | None:
    if not report:
        return None
    patterns = [
        r"ATS\s*Score[:\s]*(\d{1,3})",
        r"score[:\s]*(\d{1,3})\s*/\s*100",
        r"(\d{1,3})\s*/\s*100",
        r"(\d{1,3})\s*out\s*of\s*100",
    ]
    for pattern in patterns:
        match = re.search(pattern, report, re.IGNORECASE)
        if match:
            score = int(match.group(1))
            if 0 <= score <= 100:
                return score
    return None


def _score_gauge(score: int) -> go.Figure:
    color = "#10b981" if score >= 75 else "#f59e0b" if score >= 50 else "#ef4444"
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number+delta",
            value=score,
            domain={"x": [0, 1], "y": [0, 1]},
            title={"text": "ATS Match Score", "font": {"size": 16, "color": "#94a3b8"}},
            number={"font": {"size": 48, "color": "#f1f5f9", "family": "Inter"}},
            gauge={
                "axis": {"range": [0, 100], "tickcolor": "#334155", "tickwidth": 1},
                "bar": {"color": color, "thickness": 0.25},
                "bgcolor": "rgba(255,255,255,0.05)",
                "borderwidth": 0,
                "steps": [
                    {"range": [0, 50], "color": "rgba(239,68,68,0.1)"},
                    {"range": [50, 75], "color": "rgba(245,158,11,0.1)"},
                    {"range": [75, 100], "color": "rgba(16,185,129,0.1)"},
                ],
                "threshold": {
                    "line": {"color": color, "width": 3},
                    "thickness": 0.8,
                    "value": score,
                },
            },
        )
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=280,
        margin=dict(l=20, r=20, t=60, b=20),
        font={"family": "Inter"},
    )
    return fig


def _render_steps(current: int):
    steps = [
        (1, "📄", "Upload Resume"),
        (2, "🎯", "Add Job Details"),
        (3, "✨", "AI Generation"),
        (4, "📊", "ATS Analysis"),
    ]
    html = '<div class="steps">'
    for i, (num, icon, label) in enumerate(steps):
        if num < current:
            cls, lbl_cls = "done", ""
        elif num == current:
            cls, lbl_cls = "active", "active"
        else:
            cls, lbl_cls = "", ""
        html += f"""
        <div class="step">
            <div class="step-num {cls}">{icon if cls == 'active' else ('✓' if cls == 'done' else num)}</div>
            <span class="step-label {lbl_cls}">{label}</span>
        </div>"""
        if i < len(steps) - 1:
            conn_cls = "done" if num < current else ""
            html += f'<div class="step-connector {conn_cls}"></div>'
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)


def _render_metric_cards():
    has_resume = st.session_state["generated_resume"] is not None
    has_ats = st.session_state["ats_report"] is not None
    score = st.session_state.get("ats_score")
    gh_count = len(st.session_state.get("github_data") or [])
    build_time = st.session_state.get("last_build_time")

    score_display = f"{score}%" if score is not None else "—"
    score_delta = "Analyzed" if has_ats else "Not run yet"
    score_cls = "delta-up" if score and score >= 70 else "delta-neutral"

    st.markdown(
        f"""
        <div class="metric-grid">
            <div class="metric-card">
                <div class="metric-icon">🎯</div>
                <div class="metric-value">{score_display}</div>
                <div class="metric-label">ATS Score</div>
                <div class="metric-delta {score_cls}">{score_delta}</div>
            </div>
            <div class="metric-card">
                <div class="metric-icon">📝</div>
                <div class="metric-value">{"Ready" if has_resume else "—"}</div>
                <div class="metric-label">Resume Status</div>
                <div class="metric-delta {"delta-up" if has_resume else "delta-neutral"}">
                    {"Generated" if has_resume else "Awaiting input"}
                </div>
            </div>
            <div class="metric-card">
                <div class="metric-icon">🐙</div>
                <div class="metric-value">{gh_count}</div>
                <div class="metric-label">GitHub Projects</div>
                <div class="metric-delta delta-neutral">Fetched from profile</div>
            </div>
            <div class="metric-card">
                <div class="metric-icon">⚡</div>
                <div class="metric-value">{"Done" if build_time else "—"}</div>
                <div class="metric-label">Last Build</div>
                <div class="metric-delta delta-neutral">
                    {build_time if build_time else "No builds yet"}
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────────────────────────────────────
# Sidebar
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚡ ResumeForge")
    st.markdown(
        '<span class="status-pill pill-active">● AI Powered</span>',
        unsafe_allow_html=True,
    )
    st.markdown("---")

    st.markdown("## 📋 Job Details")
    job_description = st.text_area(
        "Job Description",
        height=220,
        placeholder="Paste the full job description here...\n\nInclude required skills, responsibilities, and qualifications for best ATS matching.",
        label_visibility="collapsed",
    )

    st.markdown("## 🔗 Profile Links")
    github_url = st.text_input(
        "GitHub URL",
        placeholder="https://github.com/yourusername",
    )
    portfolio_url = st.text_input(
        "Portfolio URL",
        placeholder="https://yourportfolio.com",
    )

    st.markdown("## 📄 Resume Upload")
    uploaded_resume = st.file_uploader(
        "Upload Resume (PDF / DOCX)",
        type=["pdf", "docx"],
        label_visibility="collapsed",
    )

    if uploaded_resume:
        st.markdown(
            '<span class="status-pill pill-ready">✓ Resume uploaded</span>',
            unsafe_allow_html=True,
        )

    st.markdown("---")

    with st.expander("⚙️ Advanced Options"):
        ai_provider = st.selectbox(
            "AI Provider",
            options=["auto", "groq", "gemini"],
            format_func=lambda x: {
                "auto": "Auto (Gemini → Groq fallback)",
                "groq": "Groq only (recommended if Gemini quota exceeded)",
                "gemini": "Gemini only",
            }[x],
            index=0,
        )
        st.caption(
            "Use **Groq** if you see Gemini 429/quota errors. "
            "Requires `GROQ_API_KEY` in `.env`."
        )
        tone = st.selectbox(
            "Writing Tone",
            ["Professional", "Confident", "Technical", "Executive"],
        )
        focus = st.multiselect(
            "Optimize For",
            ["Keywords", "Achievements", "Skills", "Projects", "Leadership"],
            default=["Keywords", "Achievements", "Skills"],
        )
        st.caption("Tone & focus preferences are passed to the AI model.")

    st.markdown("---")
    if st.button("🗑️ Reset Session", use_container_width=True):
        for key in _DEFAULTS:
            st.session_state[key] = _DEFAULTS[key]
        st.rerun()


# ─────────────────────────────────────────────────────────────────────────────
# Main layout
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="hero">
        <div class="hero-badge">Gemini + Groq · Auto-fallback enabled</div>
        <h1>ResumeForge AI</h1>
        <p>Transform your resume into an ATS-optimized, keyword-rich document tailored
        to any job description — powered by multi-agent AI orchestration.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

_render_metric_cards()

# Determine current step
if st.session_state["ats_report"]:
    current_step = 4
elif st.session_state["generated_resume"]:
    current_step = 3
elif uploaded_resume and job_description.strip():
    current_step = 2
else:
    current_step = 1

_render_steps(current_step)

# Feature cards (shown when no resume generated yet)
if not st.session_state["generated_resume"]:
    st.markdown(
        """
        <div class="feature-grid">
            <div class="feature-card">
                <div class="feature-icon">🤖</div>
                <div class="feature-title">Multi-Agent AI Pipeline</div>
                <div class="feature-desc">Tries Gemini first, then automatically falls back to Groq Llama 3.3 if quota is exceeded.</div>
            </div>
            <div class="feature-card">
                <div class="feature-icon">🔍</div>
                <div class="feature-title">Smart Keyword Injection</div>
                <div class="feature-desc">Automatically extracts and injects job-description keywords to maximize ATS pass-through rates.</div>
            </div>
            <div class="feature-card">
                <div class="feature-icon">🐙</div>
                <div class="feature-title">GitHub & Portfolio Sync</div>
                <div class="feature-desc">Pulls live project data from your GitHub repos and portfolio site to enrich your resume automatically.</div>
            </div>
            <div class="feature-card">
                <div class="feature-icon">📊</div>
                <div class="feature-title">ATS Score Dashboard</div>
                <div class="feature-desc">Get a detailed ATS match score with missing keywords and actionable improvement suggestions.</div>
            </div>
            <div class="feature-card">
                <div class="feature-icon">📥</div>
                <div class="feature-title">Multi-Format Export</div>
                <div class="feature-desc">Download your optimized resume as PDF, LaTeX, or plain text — ready for any application portal.</div>
            </div>
            <div class="feature-card">
                <div class="feature-icon">🛡️</div>
                <div class="feature-title">Prompt Injection Guard</div>
                <div class="feature-desc">Built-in safety filters and system-instruction hardening protect against malicious resume content.</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ─────────────────────────────────────────────────────────────────────────────
# Action bar
# ─────────────────────────────────────────────────────────────────────────────
action_col1, action_col2, action_col3 = st.columns([2, 2, 1])

with action_col1:
    generate_clicked = st.button(
        "✨ Generate ATS Resume",
        type="primary",
        use_container_width=True,
    )

with action_col2:
    ats_clicked = st.button(
        "📊 Run ATS Analysis",
        use_container_width=True,
    )

with action_col3:
    preview_github = st.button("🔄 Fetch Data", use_container_width=True)

# Handle fetch data
if preview_github:
    with st.spinner("Fetching GitHub & portfolio data..."):
        if github_url:
            st.session_state["github_data"] = get_github_projects(github_url)
        if portfolio_url:
            st.session_state["portfolio_data"] = get_portfolio_skills(portfolio_url)
    st.toast("Profile data refreshed!", icon="✅")

# Handle generate
if generate_clicked:
    if not job_description.strip():
        st.error("⚠️ Please enter a job description in the sidebar.")
    elif not uploaded_resume:
        st.error("⚠️ Please upload your current resume.")
    else:
        progress = st.progress(0, text="Initializing AI agents...")
        for pct, msg in [
            (15, "Parsing resume..."),
            (35, "Fetching GitHub projects..."),
            (55, "Scraping portfolio skills..."),
            (75, "Generating ATS-optimized content..."),
            (95, "Finalizing resume..."),
        ]:
            time.sleep(0.3)
            progress.progress(pct, text=msg)

        resume_text = read_resume(uploaded_resume)
        github_data = (
            st.session_state["github_data"]
            if st.session_state["github_data"]
            else (get_github_projects(github_url) if github_url else [])
        )
        portfolio_data = (
            st.session_state["portfolio_data"]
            if st.session_state["portfolio_data"]
            else (get_portfolio_skills(portfolio_url) if portfolio_url else "")
        )

        generated_resume = build_resume(
            job_description,
            github_data,
            portfolio_data,
            resume_text,
           
        )

        is_error = generated_resume.startswith((
            "Error:",
            "Configuration Error:",
            "Gemini API Error",
            "Gemini Quota Error",
            "Groq API Error",
            "Gemini quota exceeded",
        ))

        st.session_state.update({
            "generated_resume": generated_resume,
            "github_data": github_data,
            "portfolio_data": portfolio_data,
            "resume_text": resume_text,
            "last_build_time": time.strftime("%H:%M:%S"),
            "ats_report": None,
            "ats_score": None,
        })

        progress.progress(100, text="Done!")
        time.sleep(0.4)
        progress.empty()
        if is_error:
            st.error(generated_resume)
        else:
            st.toast("Resume generated successfully!", icon="🎉")
        st.rerun()

# Handle ATS analysis
if ats_clicked:
    generated_resume = st.session_state.get("generated_resume")
    if not generated_resume:
        st.error("⚠️ Generate a resume first before running ATS analysis.")
    elif not job_description.strip():
        st.error("⚠️ Please enter a job description.")
    else:
        with st.spinner("Running ATS analysis with Groq Llama 3.3..."):
            report = get_ats_report(generated_resume, job_description)
            score = _extract_ats_score(report)
            st.session_state["ats_report"] = report
            st.session_state["ats_score"] = score
        st.toast("ATS analysis complete!", icon="📊")
        st.rerun()

# ─────────────────────────────────────────────────────────────────────────────
# Results tabs
# ─────────────────────────────────────────────────────────────────────────────
if st.session_state["generated_resume"] or st.session_state["github_data"]:
    tab_preview, tab_ats, tab_export, tab_data = st.tabs(
        ["📝 Resume Preview", "📊 ATS Analysis", "📥 Export", "🔗 Source Data"]
    )

    with tab_preview:
        st.markdown('<div class="section-header">Generated Resume</div>', unsafe_allow_html=True)
        edited_resume = st.text_area(
            "Edit your resume",
            value=st.session_state["generated_resume"] or "",
            height=420,
            label_visibility="collapsed",
        )
        if edited_resume != st.session_state["generated_resume"]:
            st.session_state["generated_resume"] = edited_resume

        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.metric("Word Count", len(edited_resume.split()) if edited_resume else 0)
        with col_b:
            st.metric("Characters", len(edited_resume) if edited_resume else 0)
        with col_c:
            sections = edited_resume.lower().count("experience") + edited_resume.lower().count("skills")
            st.metric("Key Sections", sections)

    with tab_ats:
        st.markdown('<div class="section-header">ATS Compatibility Report</div>', unsafe_allow_html=True)
        if st.session_state["ats_report"]:
            score = st.session_state.get("ats_score")
            if score is not None:
                gauge_col, report_col = st.columns([1, 2])
                with gauge_col:
                    st.plotly_chart(_score_gauge(score), use_container_width=True)
                    if score >= 75:
                        st.success("Strong ATS match — ready to apply!")
                    elif score >= 50:
                        st.warning("Moderate match — review missing keywords below.")
                    else:
                        st.error("Low match — significant improvements needed.")
                with report_col:
                    st.markdown(st.session_state["ats_report"])
            else:
                st.markdown(st.session_state["ats_report"])
        else:
            st.info("Click **Run ATS Analysis** to get your compatibility score and improvement suggestions.")

    with tab_export:
        st.markdown('<div class="section-header">Download Your Resume</div>', unsafe_allow_html=True)
        resume_content = st.session_state.get("generated_resume", "")

        exp_col1, exp_col2, exp_col3 = st.columns(3)

        with exp_col1:
            st.markdown("**📄 Plain Text**")
            st.download_button(
                "Download .txt",
                data=resume_content,
                file_name="resume.txt",
                mime="text/plain",
                use_container_width=True,
            )

        with exp_col2:
            st.markdown("**📐 LaTeX**")
            latex_content = generate_latex(resume_content)
            st.download_button(
                "Download .tex",
                data=latex_content,
                file_name="resume.tex",
                mime="text/plain",
                use_container_width=True,
            )

        with exp_col3:
            st.markdown("**📕 PDF**")
            if st.button("Generate PDF", use_container_width=True):
                with st.spinner("Compiling PDF..."):
                    try:
                        pdf_path = generate_pdf(resume_content)
                        with open(pdf_path, "rb") as pdf_file:
                            st.download_button(
                                "Download .pdf",
                                data=pdf_file.read(),
                                file_name="resume.pdf",
                                mime="application/pdf",
                                use_container_width=True,
                            )
                    except Exception as error:
                        st.warning(
                            f"PDF generation failed. Install MiKTeX or TeX Live. Details: {error}"
                        )

        st.markdown("---")
        st.markdown("**Quick Copy**")
        st.code(resume_content[:2000] + ("..." if len(resume_content) > 2000 else ""), language=None)

    with tab_data:
        st.markdown('<div class="section-header">Source Data Used</div>', unsafe_allow_html=True)
        data_col1, data_col2 = st.columns(2)

        with data_col1:
            st.markdown("**🐙 GitHub Projects**")
            gh = st.session_state.get("github_data") or []
            if gh:
                chips = ""
                for proj in gh:
                    name = proj.get("name", "?")
                    lang = proj.get("language") or "N/A"
                    chips += f'<span class="project-chip">{name} <span class="lang-badge">{lang}</span></span>'
                st.markdown(chips, unsafe_allow_html=True)
            else:
                st.caption("No GitHub data fetched. Add a GitHub URL and click Fetch Data.")

        with data_col2:
            st.markdown("**🌐 Portfolio Skills**")
            portfolio = st.session_state.get("portfolio_data", "")
            if portfolio:
                st.text_area(
                    "Portfolio excerpt",
                    value=portfolio[:1500],
                    height=200,
                    disabled=True,
                    label_visibility="collapsed",
                )
            else:
                st.caption("No portfolio data fetched. Add a portfolio URL and click Fetch Data.")

# ─────────────────────────────────────────────────────────────────────────────
# Footer
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="footer">
        ResumeForge AI &nbsp;·&nbsp; Built with Streamlit + Gemini + Groq &nbsp;·&nbsp;
        ATS-Optimized Resume Generation
    </div>
    """,
    unsafe_allow_html=True,
)
