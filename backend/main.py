from fastapi import FastAPI
from pydantic import BaseModel
from utils import extract_jd_skills, extract_resume_skills, calculate_score

app = FastAPI()


# =========================
# 📥 INPUT SCHEMA
# =========================
class InputData(BaseModel):
    resume_text: str
    job_description: str


# =========================
# 🏠 HEALTH CHECK
# =========================
@app.get("/")
def home():
    return {"message": "AI Career Copilot API is running 🚀"}


# =========================
# 🔍 ANALYZE ENDPOINT
# =========================
@app.post("/analyze")
def analyze(data: InputData):
    print("\n==========================")
    print("RESUME TEXT:", data.resume_text[:200])

    # =========================
    # 🔥 EXTRACT SKILLS
    # =========================
    jd_skills = extract_jd_skills(data.job_description)
    resume_skills = extract_resume_skills(data.resume_text)

    print("JD SKILLS:", jd_skills)
    print("RESUME SKILLS:", resume_skills)

    # fallback if JD parsing fails
    if not jd_skills:
        return {
            "score": 0,
            "matched": [],
            "missing": [],
            "error": "Could not extract skills from job description"
        }

    jd_set = set(jd_skills)
    resume_set = set(resume_skills)

    # =========================
    # 🔥 MATCH ENGINE
    # =========================
    matched = list(jd_set & resume_set)
    missing = list(jd_set - resume_set)

    # =========================
    # 🔥 SMART MATCH (important basics)
    # =========================
    for skill in ["python", "git"]:
        if skill in resume_set and skill not in matched:
            matched.append(skill)

    # =========================
    # 🔥 PRIORITY SORT
    # =========================
    priority = {
        "django": 3,
        "api": 3,
        "llm": 3,
        "postgres": 2,
        "langchain": 2,
        "prompt": 2,
        "git": 1,
        "python": 1
    }

    matched = sorted(
        matched,
        key=lambda x: priority.get(x, 1),
        reverse=True
    )

    missing = sorted(
        missing,
        key=lambda x: priority.get(x, 1),
        reverse=True
    )

    # =========================
    # 🔥 LIMIT OUTPUT (UI CLEAN)
    # =========================
    matched = matched[:3]
    missing = missing[:3]

    print("MATCHED:", matched)
    print("MISSING:", missing)

    # =========================
    # 🔥 SCORE
    # =========================
    score = calculate_score(jd_skills, matched)

    return {
        "score": score,
        "matched": matched,
        "missing": missing
    }