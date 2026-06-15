# ResumeForgeAI-Multi-Agent-ATS-Resume-Builder-
# 🚀 ResumeForge AI

### AI-Powered Multi-Agent ATS Resume Builder

ResumeForge AI is an intelligent resume generation platform that creates ATS-optimized resumes tailored to specific job descriptions using AI Agents and Large Language Models (LLMs).

The system analyzes job descriptions, extracts relevant skills and keywords, evaluates GitHub projects and portfolio information, and generates professional resumes with downloadable PDF support.

---

## ✨ Features

### 📄 ATS Resume Generation

* Generate ATS-friendly resumes from job descriptions.
* Optimized keyword matching for higher recruiter visibility.
* Professional resume formatting.

### 🤖 AI-Powered Resume Writing

* Uses Groq LLM for intelligent resume generation.
* Tailors skills, projects, and summaries to job requirements.
* Generates recruiter-friendly content automatically.

### 💻 GitHub Profile Analysis

* Extracts repositories and technologies.
* Identifies relevant projects for inclusion in resumes.
* Highlights technical experience.

### 🌐 Portfolio Analysis

* Reads portfolio website content.
* Extracts skills, projects, and achievements.
* Enhances resume relevance.

### 📊 ATS Score Analysis

* Matches resume against job description.
* Identifies missing keywords.
* Provides optimization suggestions.

### 📑 PDF Resume Export

* Generates clean ATS-compatible PDF resumes.
* Professional formatting using ReportLab.
* One-click download functionality.

---

## 🏗️ System Architecture

Job Description
↓
GitHub Analyzer Agent
↓
Portfolio Analyzer Agent
↓
Resume Generation Agent (Groq)
↓
ATS Score Agent
↓
PDF Generator
↓
Download Resume

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

ResumeForge-AI/

├── agents/

│ ├── groq_agent.py

│ ├── github_agent.py

│ ├── portfolio_agent.py

│ ├── ats_agent.py

│ └── resume_agent.py

├── utils/

│ ├── parser.py

│ ├── pdf_generator.py

│ └── latex_generator.py

├── generated/

├── app.py

├── requirements.txt

├── .env.example

├── .gitignore

└── README.md

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

Windows

```bash
venv\Scripts\activate
```

Linux/Mac

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

* Multi-Agent Workflow using LangGraph
* Resume Version History
* LinkedIn Profile Integration
* Vector Database Memory
* AI Interview Preparation
* Multi-Format Resume Templates
* Cover Letter Generator
* Recruiter Dashboard

---

## 👨‍💻 Author

Vaibhav Sable

Generative AI Developer

GitHub: https://github.com/Vaibhavsable451

LinkedIn: https://www.linkedin.com/in/vaibhavsable-software-engineer

Portfolio: https://portfolio-vkkz.onrender.com

---

⭐ If you found this project useful, please give it a star.
