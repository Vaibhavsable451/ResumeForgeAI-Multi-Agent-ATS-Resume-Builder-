import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER


# ── Styles ──────────────────────────────────────────────────────────────────

def _build_styles():
    base = getSampleStyleSheet()

    name_style = ParagraphStyle(
        "Name",
        parent=base["Normal"],
        fontSize=18,
        fontName="Helvetica-Bold",
        textColor=colors.HexColor("#1a1a2e"),
        alignment=TA_CENTER,
        spaceAfter=2,
    )
    contact_style = ParagraphStyle(
        "Contact",
        parent=base["Normal"],
        fontSize=8.5,
        fontName="Helvetica",
        textColor=colors.HexColor("#444444"),
        alignment=TA_CENTER,
        spaceAfter=6,
    )
    section_style = ParagraphStyle(
        "Section",
        parent=base["Normal"],
        fontSize=10.5,
        fontName="Helvetica-Bold",
        textColor=colors.HexColor("#1a1a2e"),
        spaceBefore=10,
        spaceAfter=2,
    )
    job_title_style = ParagraphStyle(
        "JobTitle",
        parent=base["Normal"],
        fontSize=9.5,
        fontName="Helvetica-Bold",
        textColor=colors.HexColor("#222222"),
        spaceAfter=1,
    )
    date_style = ParagraphStyle(
        "Date",
        parent=base["Normal"],
        fontSize=9,
        fontName="Helvetica-Oblique",
        textColor=colors.HexColor("#555555"),
        alignment=TA_LEFT,
    )
    body_style = ParagraphStyle(
        "Body",
        parent=base["Normal"],
        fontSize=9,
        fontName="Helvetica",
        textColor=colors.HexColor("#333333"),
        leading=13,
        spaceAfter=2,
    )
    bullet_style = ParagraphStyle(
        "Bullet",
        parent=base["Normal"],
        fontSize=9,
        fontName="Helvetica",
        textColor=colors.HexColor("#333333"),
        leading=13,
        leftIndent=12,
        bulletIndent=0,
        spaceAfter=1,
    )
    subheading_style = ParagraphStyle(
        "Subheading",
        parent=base["Normal"],
        fontSize=9,
        fontName="Helvetica-Bold",
        textColor=colors.HexColor("#333333"),
        spaceAfter=1,
    )
    return {
        "name": name_style,
        "contact": contact_style,
        "section": section_style,
        "job_title": job_title_style,
        "date": date_style,
        "body": body_style,
        "bullet": bullet_style,
        "subheading": subheading_style,
    }


def _divider():
    return HRFlowable(
        width="100%",
        thickness=0.8,
        color=colors.HexColor("#1a1a2e"),
        spaceAfter=4,
    )


def _section_header(title, styles):
    return [
        Paragraph(title.upper(), styles["section"]),
        _divider(),
    ]


# ── Resume parser → structured PDF ──────────────────────────────────────────

def generate_pdf_from_data(resume_data: dict, output_path: str) -> str:
    """
    resume_data keys:
        name, title, contact (dict: email, phone, linkedin, github, portfolio),
        summary, skills (list of dicts: {category, items}),
        experience (list of dicts: {title, company, location, dates, bullets}),
        projects (list of dicts: {name, tech, bullets}),
        certifications (list of str),
        education (list of dicts: {degree, institution, dates, grade})
    """
    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".", exist_ok=True)

    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=0.6 * inch,
        rightMargin=0.6 * inch,
        topMargin=0.5 * inch,
        bottomMargin=0.5 * inch,
    )

    styles = _build_styles()
    story = []

    # ── Header ──
    story.append(Paragraph(resume_data.get("name", ""), styles["name"]))
    if resume_data.get("title"):
        story.append(Paragraph(resume_data["title"], styles["contact"]))

    c = resume_data.get("contact", {})
    contact_parts = []
    if c.get("phone"):   contact_parts.append(c["phone"])
    if c.get("email"):   contact_parts.append(c["email"])
    if c.get("linkedin"):contact_parts.append(c["linkedin"])
    if c.get("github"):  contact_parts.append(c["github"])
    if c.get("portfolio"):contact_parts.append(c["portfolio"])
    story.append(Paragraph(" • ".join(contact_parts), styles["contact"]))
    story.append(Spacer(1, 4))

    # ── Summary ──
    if resume_data.get("summary"):
        story += _section_header("Professional Summary", styles)
        story.append(Paragraph(resume_data["summary"], styles["body"]))
        story.append(Spacer(1, 4))

    # ── Skills ──
    if resume_data.get("skills"):
        story += _section_header("Technical Skills", styles)
        for skill_group in resume_data["skills"]:
            line = f"<b>{skill_group['category']}:</b> {skill_group['items']}"
            story.append(Paragraph(line, styles["body"]))
        story.append(Spacer(1, 4))

    # ── Experience ──
    if resume_data.get("experience"):
        story += _section_header("Experience", styles)
        for exp in resume_data["experience"]:
            # Title + Date on same row
            data = [[
                Paragraph(f"<b>{exp['title']}</b> — {exp['company']}, {exp.get('location','')}", styles["job_title"]),
                Paragraph(exp.get("dates", ""), styles["date"]),
            ]]
            t = Table(data, colWidths=[4.2 * inch, 2.5 * inch])
            t.setStyle(TableStyle([("ALIGN", (1, 0), (1, 0), "RIGHT"), ("VALIGN", (0, 0), (-1, -1), "TOP")]))
            story.append(t)
            for b in exp.get("bullets", []):
                story.append(Paragraph(f"• {b}", styles["bullet"]))
            story.append(Spacer(1, 4))

    # ── Projects ──
    if resume_data.get("projects"):
        story += _section_header("Projects", styles)
        for proj in resume_data["projects"]:
            story.append(Paragraph(f"<b>{proj['name']}</b>  |  <i>{proj.get('tech','')}</i>", styles["job_title"]))
            for b in proj.get("bullets", []):
                story.append(Paragraph(f"• {b}", styles["bullet"]))
            story.append(Spacer(1, 4))

    # ── Certifications ──
    if resume_data.get("certifications"):
        story += _section_header("Awards & Certifications", styles)
        for cert in resume_data["certifications"]:
            story.append(Paragraph(f"• {cert}", styles["bullet"]))
        story.append(Spacer(1, 4))

    # ── Education ──
    if resume_data.get("education"):
        story += _section_header("Education", styles)
        for edu in resume_data["education"]:
            data = [[
                Paragraph(f"<b>{edu['degree']}</b> — {edu['institution']}", styles["job_title"]),
                Paragraph(edu.get("dates", ""), styles["date"]),
            ]]
            t = Table(data, colWidths=[4.2 * inch, 2.5 * inch])
            t.setStyle(TableStyle([("ALIGN", (1, 0), (1, 0), "RIGHT"), ("VALIGN", (0, 0), (-1, -1), "TOP")]))
            story.append(t)
            if edu.get("grade"):
                story.append(Paragraph(f"CGPA: {edu['grade']}", styles["body"]))
            story.append(Spacer(1, 4))

    doc.build(story)
    return output_path


# ── Drop-in replacement for old generate_pdf(resume_text) ───────────────────

def generate_pdf(resume_text: str) -> str:
    """
    Parses markdown-style resume text (output from Gemini/Groq)
    and generates a clean ATS PDF. Returns path to the PDF.
    """
    os.makedirs("generated", exist_ok=True)

    resume_data = _parse_resume_text(resume_text)
    output_path = "generated/resume.pdf"
    return generate_pdf_from_data(resume_data, output_path)


def _parse_resume_text(text: str) -> dict:
    """
    Parses the markdown resume text produced by LLM agents into
    a structured dict for generate_pdf_from_data().
    """
    import re

    data = {
        "name": "",
        "title": "",
        "contact": {},
        "summary": "",
        "skills": [],
        "experience": [],
        "projects": [],
        "certifications": [],
        "education": [],
    }

    lines = text.splitlines()
    current_section = None
    buffer = []

    def flush_buffer(section, buf):
        """Process buffered lines for a section."""
        if section == "summary":
            data["summary"] = " ".join(
                l.strip().lstrip("*#-_").strip() for l in buf if l.strip()
            )
        elif section == "skills":
            for line in buf:
                line = line.strip().lstrip("*•–- ").strip()
                if ":" in line:
                    cat, items = line.split(":", 1)
                    data["skills"].append({
                        "category": cat.strip().strip("*#_"),
                        "items": items.strip()
                    })
        elif section == "experience":
            _parse_experience(buf, data)
        elif section == "projects":
            _parse_projects(buf, data)
        elif section == "certifications":
            for line in buf:
                line = line.strip().lstrip("*•– -").strip()
                if line:
                    data["certifications"].append(line)
        elif section == "education":
            _parse_education(buf, data)

    section_map = {
        "professional summary": "summary",
        "summary": "summary",
        "technical skills": "skills",
        "skills": "skills",
        "experience": "experience",
        "work experience": "experience",
        "projects": "projects",
        "awards": "certifications",
        "certifications": "certifications",
        "awards & certifications": "certifications",
        "education": "education",
    }

    header_done = False

    for i, line in enumerate(lines):
        stripped = line.strip()

        # Skip LLM preamble lines and UI metadata
        if stripped.startswith("[") and (stripped.endswith("]") or "fallback" in stripped.lower() or "groq" in stripped.lower() or "gemini" in stripped.lower()):
            continue
        # Also skip lines like "Here's an optimized ATS-friendly resume:"
        if "here's" in stripped.lower() and "resume" in stripped.lower():
            continue
        if "ats-optimized resume" in stripped.lower():
            continue

        # Detect section headers
        clean = stripped.strip("*#_ ").strip()
        lower = clean.lower()

        matched_section = None
        for key, val in section_map.items():
            if lower == key or lower == key + ":":
                matched_section = val
                break

        if matched_section:
            # Flush previous buffer
            if current_section and buffer:
                flush_buffer(current_section, buffer)
            current_section = matched_section
            buffer = []
            header_done = True
            continue

        # Parse header (name, title, contact) before first section
        if not header_done:
            clean_line = stripped.strip("*#_ ").strip()
            if not clean_line:
                continue

            # If it's a contact line, parse it
            if "@" in clean_line or any(c in clean_line.lower() for c in ["linkedin", "github", "portfolio", "phone", "email", "+91"]):
                _parse_contact_line(clean_line, data["contact"])
            # If we don't have a name yet, set it
            elif not data["name"] and lower not in section_map:
                data["name"] = clean_line
            # If we have name but no title, set it
            elif not data["title"] and lower not in section_map:
                data["title"] = clean_line
            continue

        if current_section:
            buffer.append(line)

    # Flush last section
    if current_section and buffer:
        flush_buffer(current_section, buffer)

    return data


def _parse_contact_line(line, contact):
    import re
    line = line.strip().lstrip("*•– ").strip()
    parts = re.split(r"\s*[•|]\s*", line)
    for p in parts:
        p = p.strip()
        if not p:
            continue
        if "@" in p:
            contact["email"] = p
        elif "linkedin.com" in p.lower() or "linkedin" in p.lower():
            contact["linkedin"] = p
        elif "github.com" in p.lower() or "github" in p.lower():
            contact["github"] = p
        elif "portfolio" in p.lower() or "render" in p.lower() or "vercel" in p.lower() or "portfolio-vkkz" in p.lower():
            contact["portfolio"] = p
        elif any(c.isdigit() for c in p) and len([c for c in p if c.isdigit()]) >= 8:
            contact["phone"] = p


def _is_bullet(line: str) -> bool:
    stripped = line.strip()
    if not stripped:
        return False
    if stripped.startswith("**") or stripped.startswith("* **") or stripped.startswith("- **") or stripped.startswith("– **"):
        return False
    if stripped.startswith(("-", "•", "–", "—", "+")):
        return True
    if stripped.startswith("* "):
        return True
    return False


def _parse_experience(lines, data):
    import re
    current = None
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue

        if _is_bullet(line):
            if current:
                bullet = stripped.lstrip("-*•–—+ ").strip()
                if bullet:
                    current["bullets"].append(bullet)
        else:
            # New job entry
            if current:
                data["experience"].append(current)

            clean = stripped.replace("**", "").replace("_", "").strip("*#_ ").strip()
            # Find date range (e.g., "Jun 2025 – Dec 2025" or "2023 - 2025" or "Present")
            date_match = re.search(r"\(?\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|20\d\d|Present)\b.*", clean, re.IGNORECASE)
            dates = date_match.group(0).strip("() ") if date_match else ""

            title_part = clean[:date_match.start()].strip(" |–-() ") if date_match else clean
            # Split title, company, location by common separators (using word boundaries for 'at')
            parts = re.split(r"\s*(?:\||\bat\b|–|-|,)\s*", title_part)

            current = {
                "title": parts[0].strip() if parts else title_part,
                "company": parts[1].strip() if len(parts) > 1 else "",
                "location": parts[2].strip() if len(parts) > 2 else "",
                "dates": dates,
                "bullets": []
            }
    if current:
        data["experience"].append(current)


def _parse_projects(lines, data):
    current = None
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue

        if _is_bullet(line):
            if current:
                bullet = stripped.lstrip("-*•–—+ ").strip()
                if bullet:
                    current["bullets"].append(bullet)
        else:
            if current:
                data["projects"].append(current)
            clean = stripped.replace("**", "").replace("_", "").strip("*#_ ").strip()
            # Split project name and tech stack by pipe or dash or colon
            parts = re.split(r"\s*(?:\||:|\s-\s)\s*", clean)
            current = {
                "name": parts[0].strip(),
                "tech": parts[1].strip() if len(parts) > 1 else "",
                "bullets": []
            }
    if current:
        data["projects"].append(current)


def _parse_education(lines, data):
    import re
    current = None
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue

        if _is_bullet(line):
            bullet = stripped.lstrip("-*•–—+ ").strip()
            if current and ("cgpa" in bullet.lower() or "gpa" in bullet.lower() or "%" in bullet or "grade" in bullet.lower()):
                current["grade"] = bullet
        else:
            if current:
                data["education"].append(current)
            clean = stripped.replace("**", "").replace("_", "").strip("*#_ ").strip()

            # Find date range
            date_match = re.search(r"\(?\b(20\d\d\s*[–-]\s*(?:20\d\d|Present)|\b20\d\d\b)\)?", clean)
            dates_str = date_match.group(0).strip("() ") if date_match else ""
            title_part = clean[:date_match.start()].strip(" |–-") if date_match else clean

            parts = re.split(r"\s*(?:\||\bat\b|–|-|,)\s*", title_part)
            current = {
                "degree": parts[0].strip() if parts else title_part,
                "institution": parts[1].strip() if len(parts) > 1 else "",
                "dates": dates_str,
                "grade": ""
            }
    if current:
        data["education"].append(current)


# ── Quick test ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    sample = {
        "name": "Vaibhav Sable",
        "title": "Generative AI Developer",
        "contact": {
            "phone": "+91-9373012758",
            "email": "vaibhavsable150@gmail.com",
            "linkedin": "linkedin.com/in/vaibhavsable-software-engineer",
            "github": "github.com/Vaibhavsable451",
            "portfolio": "portfolio-vkkz.onrender.com",
        },
        "summary": (
            "AI Engineer skilled in Generative AI, LLMs, RAG, Agentic AI, and NLP. "
            "Experienced in building AI-powered applications and automation systems "
            "using Python, LangChain, and LLM APIs."
        ),
        "skills": [
            {"category": "Programming Languages", "items": "Python"},
            {"category": "AI / Machine Learning", "items": "LLMs, RAG, Agentic AI, NLP, Prompt Engineering, Embeddings"},
            {"category": "AI Frameworks", "items": "LangChain, LangGraph, CrewAI, OpenAI API, Gemini API, Groq"},
            {"category": "Databases & Vector Stores", "items": "MySQL, FAISS, Pinecone"},
            {"category": "Backend & Cloud", "items": "FastAPI, REST APIs, GCP, Docker, CI/CD"},
            {"category": "Tools", "items": "Git, GitHub, Postman, VS Code, n8n"},
        ],
        "experience": [
            {
                "title": "Data Science Intern",
                "company": "Internship Studio",
                "location": "Remote, Pune",
                "dates": "Jun 2025 – Dec 2025",
                "bullets": [
                    "Designed and implemented ETL data pipelines using Python and SQL, improving data processing efficiency by 25%.",
                    "Developed automated data workflows and reporting systems using Python, reducing manual effort across business units.",
                    "Applied Machine Learning techniques and data visualization tools to extract meaningful patterns from structured and unstructured datasets.",
                    "Built data-driven insights and dashboards to support decision-making for cross-functional stakeholders.",
                ],
            }
        ],
        "projects": [
            {
                "name": "Multi-Agent AI Research System",
                "tech": "Python, LangChain, Groq LLM, Streamlit, BeautifulSoup",
                "bullets": [
                    "Built a Multi-Agent AI system using LangChain and Groq LLMs to automate end-to-end research workflows.",
                    "Designed specialized AI agents: Search Agent, Reader Agent, Writer Chain, and Critic Chain.",
                    "Implemented web scraping and content extraction pipelines using BeautifulSoup and Requests.",
                    "Deployed as an interactive Streamlit web application with user-friendly interface.",
                ],
            },
            {
                "name": "Q&A AI Agent with RAG using n8n",
                "tech": "n8n, Gemini, Pinecone, RAG, Google Cloud",
                "bullets": [
                    "Built a no-code RAG-based AI Q&A system using n8n workflows and Google Gemini.",
                    "Integrated Google Drive for document ingestion and Pinecone for vector storage and retrieval.",
                    "Implemented chunking, embeddings, and semantic search for accurate contextual responses.",
                ],
            },
        ],
        "certifications": [
            "Automate Everything With n8n – LetsUpgrade",
            "Anthropic Certified – Claude API, MCP, Bedrock, Vertex AI, AI Fluency, Agentic AI Systems",
            "Solved 50+ Data Structures and Algorithms problems on LeetCode",
        ],
        "education": [
            {"degree": "Master of Computer Applications (MCA)", "institution": "Pimpri Chinchwad University, Pune", "dates": "2023 – 2025", "grade": "7.3/10"},
            {"degree": "Bachelor of Computer Applications (BCA)", "institution": "Savitribai Phule Pune University, Pune", "dates": "2020 – 2023", "grade": "7.0/10"},
        ],
    }

    path = generate_pdf_from_data(sample, "generated/vaibhav_sable_resume.pdf")
    print(f"PDF generated: {path}")
