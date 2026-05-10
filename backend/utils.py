# backend/utils.py
import re


# =========================
# 🔥 NORMALIZE
# =========================
def normalize(skills):
    return list(set([s.lower().strip() for s in skills if s]))


# =========================
# 🔥 TEXT CLEANER
# =========================
def clean_text(text):
    return re.sub(r"[^\w\s]", " ", text.lower())


# =========================
# 🔥 WORD MATCH (STRICT)
# =========================
def contains_word(text, word):
    return word in text.split()


# =========================
# 🔥 MULTI WORD MATCH
# =========================
def contains_any(text, words):
    tokens = text.split()
    return any(word in tokens for word in words)


# =========================
# 🔥 JD SKILLS
# =========================
def extract_jd_skills(job_desc):
    jd = clean_text(job_desc)
    skills = []

    if contains_word(jd, "python"):
        skills.append("python")

    if contains_word(jd, "django"):
        skills.append("django")

    # ✅ API detection (strict)
    if contains_any(jd, ["api", "rest", "fastapi", "backend"]):
        skills.append("api")

    # ✅ LLM detection (STRICT — removed generic "ai")
    if contains_any(jd, ["openai", "claude", "gemini", "llm", "gpt", "langchain"]):
        skills.append("llm")

    if contains_any(jd, ["git", "github"]):
        skills.append("git")

    if contains_any(jd, ["postgres", "sql", "database"]):
        skills.append("postgres")

    if contains_word(jd, "prompt"):
        skills.append("prompt")

    if contains_word(jd, "langchain"):
        skills.append("langchain")

    if contains_word(jd, "azure"):
        skills.append("azure")

    return normalize(skills)


# =========================
# 🔥 RESUME SKILLS
# =========================
def extract_resume_skills(resume):
    text = clean_text(resume)
    skills = []

    if contains_word(text, "python"):
        skills.append("python")

    if contains_word(text, "django"):
        skills.append("django")

    if contains_any(text, ["api", "rest", "fastapi", "flask"]):
        skills.append("api")

    if contains_any(text, ["git", "github"]):
        skills.append("git")

    if contains_any(text, ["postgres", "sql"]):
        skills.append("postgres")

    # ✅ strict LLM detection
    if contains_any(text, ["openai", "llm", "langchain", "gpt"]):
        skills.append("llm")

    if contains_word(text, "prompt"):
        skills.append("prompt")

    return normalize(skills)


# =========================
# 🔥 SCORE ENGINE (BALANCED)
# =========================
def calculate_score(jd_skills, matched):
    if not jd_skills:
        return 0

    jd_set = set(jd_skills)
    matched_set = set(matched)

    base = 30

    # 🔥 Core importance
    if "python" in matched_set:
        base += 20

    if "api" in matched_set or "django" in matched_set:
        base += 15

    if "llm" in matched_set:
        base += 10

    # 🔥 Match ratio
    ratio_score = int((len(matched_set) / len(jd_set)) * 25)

    score = base + ratio_score

    return min(score, 95)