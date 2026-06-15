# ResumeForgeAI-Multi-Agent-ATS-Resume-Builder-
# ResumeForge AI 🚀

## AI-Powered Multi-Agent ATS Resume Builder

ResumeForge AI is an intelligent resume generation platform that creates ATS-optimized resumes tailored to specific job descriptions using AI Agents and Large Language Models (LLMs).

The platform analyzes job descriptions, GitHub projects, portfolio information, and existing resumes to generate professional, recruiter-friendly resumes with ATS score analysis and PDF export functionality.

---

## ✨ Key Features

### 📄 ATS Resume Generation

* Generate ATS-friendly resumes from job descriptions.
* Optimize keyword matching for recruiter visibility.
* Professional resume formatting.

### 🤖 AI-Powered Resume Writing

* Powered by Groq LLM.
* Tailors resume content according to job requirements.
* Generates professional summaries, skills, and project descriptions.

### 💻 GitHub Profile Analysis

* Extracts repositories and technologies.
* Identifies relevant projects automatically.
* Highlights technical expertise.

### 🌐 Portfolio Analysis

* Reads portfolio website content.
* Extracts skills, projects, and achievements.
* Improves resume relevance.

### 📊 ATS Score Analysis

* Matches resume against job description.
* Detects missing keywords.
* Provides ATS improvement recommendations.

### 📑 PDF Resume Export

* Generates clean ATS-compatible PDF resumes.
* Professional formatting using ReportLab.
* One-click PDF download.

---

## 🏗️ Multi-Agent Architecture

```text
Job Description
        │
        ▼
JD Analysis Agent
        │
        ▼
GitHub Analyzer Agent
        │
        ▼
Portfolio Analyzer Agent
        │
        ▼
Resume Generation Agent (Groq)
        │
        ▼
ATS Score Agent
        │
        ▼
PDF Generator Agent
        │
        ▼
Download ATS Resume
```

---

## 🛠️ Tech Stack

### Frontend

* Streamlit

### AI & LLM

* Groq API
* Llama Models

### Backend

* Python

### PDF Generation

* ReportLab

### Data Processing

* Requests
* BeautifulSoup

### Version Control

* Git
* GitHub

---

## 📂 Project Structure

```text
ResumeForgeAI/

├── agents/
│   ├── groq_agent.py
│   ├── github_agent.py
│   ├── portfolio_agent.py
│   ├── ats_agent.py
│   └── resume_agent.py
│
├── utils/
│   ├── parser.py
│   ├── pdf_generator.py
│   └── latex_generator.py
│
├── generated/
│
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/Vaibhavsable451/ResumeForgeAI-Multi-Agent-ATS-Resume-Builder-.git
cd ResumeForgeAI-Multi-Agent-ATS-Resume-Builder-
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

#### Windows

```bash
venv\Scripts\activate
```

#### Linux / Mac

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
```

---

## ▶️ Run Application

```bash
streamlit run app.py
```

---

## 📸 Workflow

1. Paste Job Description
2. Enter GitHub Profile URL
3. Enter Portfolio URL
4. Upload Existing Resume (Optional)
5. Generate ATS Resume
6. View ATS Score
7. Download PDF Resume

---

## 🎯 Future Enhancements

* LangGraph Multi-Agent Workflow
* LinkedIn Profile Integration
* Resume Version History
* Vector Database Memory
* AI Interview Preparation
* Multiple Resume Templates
* Cover Letter Generator
* Recruiter Dashboard
* Skill Gap Analysis
* Keyword Match Visualization

---

## 👨‍💻 Author

**Vaibhav Sable**

Generative AI Developer | AI Agents | RAG | LLMs | Groq | Streamlit

GitHub: https://github.com/Vaibhavsable451

LinkedIn: https://www.linkedin.com/in/vaibhavsable-software-engineer

Portfolio: https://portfolio-vkkz.onrender.com

---

## ⭐ Support

If you found this project useful, please consider giving it a Star on GitHub.
