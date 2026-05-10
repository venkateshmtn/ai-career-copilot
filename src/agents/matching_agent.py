def analyze_resume(resume_text, job_description):
    resume_text = resume_text.lower()
    job_description = job_description.lower()

    skills = [
        "python", "django", "api", "sql",
        "llm", "langchain", "postgres", "git", "prompt"
    ]

    matched = []
    missing = []
    job_skills = []

    # 🔥 Extract only skills present in job description
    for skill in skills:
        if skill in job_description:
            job_skills.append(skill)

    # 🔥 Match against resume
    for skill in job_skills:
        if skill in resume_text:
            matched.append(skill)
        else:
            missing.append(skill)

    # 🔥 Better scoring
    if len(job_skills) == 0:
        score = 0
    else:
        score = int((len(matched) / len(job_skills)) * 100)

    return {
        "score": score,
        "matched": matched,
        "missing": missing
    }