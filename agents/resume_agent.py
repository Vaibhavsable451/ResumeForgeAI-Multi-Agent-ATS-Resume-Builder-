from agents import groq_agent


def _format_github_data(github_data) -> str:
    if isinstance(github_data, str):
        return github_data

    if not github_data:
        return "No GitHub projects found."

    lines = []
    for project in github_data:
        if isinstance(project, dict):
            name = project.get("name", "Unknown project")
            language = project.get("language") or "N/A"
            lines.append(f"- {name} ({language})")
        else:
            lines.append(str(project))

    return "\n".join(lines)


def build_resume(jd, github_data, portfolio_data, old_resume):
    github_projects = _format_github_data(github_data)

    try:
        result = groq_agent.generate_resume(
            job_description=jd,
            github_projects=github_projects,
            portfolio_skills=portfolio_data,
            resume_text=old_resume,
        )

        return (
            f"[Generated with Groq: {groq_agent.GROQ_RESUME_MODEL}]\n\n"
            f"{result}"
        )

    except ValueError as exc:
        return f"Configuration Error: {exc}"

    except Exception as exc:
        return f"Groq API Error: {type(exc).__name__}: {exc}"