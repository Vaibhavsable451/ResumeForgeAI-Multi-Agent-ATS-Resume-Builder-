from agents.groq_agent import calculate_ats_score


def get_ats_report(
        resume,
        jd):

    return calculate_ats_score(
        resume,
        jd
    )