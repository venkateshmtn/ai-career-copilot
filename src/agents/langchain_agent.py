from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import CharacterTextSplitter


# =========================
# 🔥 SKILL NORMALIZATION MAP
# =========================
SKILL_MAP = {

    "python": [
        "python"
    ],

    "django": [
        "django",
        "django rest framework",
        "drf"
    ],

    "api": [
        "api",
        "apis",
        "rest api",
        "rest apis",
        "fastapi",
        "backend api"
    ],

    "langchain": [
        "langchain",
        "chains",
        "rag pipeline"
    ],

    "llm": [
        "llm",
        "llms",
        "large language model",
        "large language models",
        "gpt",
        "transformers"
    ],

    "genai": [
        "generative ai",
        "genai",
        "rag",
        "ai agents"
    ],

    "openai": [
        "openai",
        "openai api",
        "chatgpt",
        "gpt-4"
    ],

    "sql": [
        "sql",
        "mysql",
        "postgresql",
        "postgres"
    ],

    "embeddings": [
        "embeddings",
        "vector embeddings"
    ],

    "faiss": [
        "faiss",
        "vector database",
        "vector search"
    ],

    "streamlit": [
        "streamlit"
    ],

    "machine learning": [
        "machine learning",
        "ml",
        "scikit-learn"
    ],

    "fastapi": [
        "fastapi"
    ]
}


# =========================
# 🔥 NORMALIZED SKILL EXTRACTION
# =========================
def extract_skills(text):

    if not text:
        return []

    text = text.lower()

    found = set()

    for main_skill, aliases in SKILL_MAP.items():

        for alias in aliases:

            alias = alias.lower().strip()

            # safer matching
            if alias in text:
                found.add(main_skill)

    return sorted(list(found))


# =========================
# 🔥 MAIN ANALYZER
# =========================
def analyze_resume_with_langchain(
    resume_text,
    job_description,
    llm=None
):

    # =========================
    # 🔹 SAFETY CHECKS
    # =========================
    resume_text = resume_text or ""
    job_description = job_description or ""

    # =========================
    # 🔹 TEXT SPLITTING
    # =========================
    splitter = CharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    docs = splitter.create_documents([
        resume_text,
        job_description
    ])

    # =========================
    # 🔹 EMBEDDINGS + VECTORSTORE
    # =========================
    try:

        embeddings = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2"
        )

        vectorstore = FAISS.from_documents(
            docs,
            embeddings
        )

        # optional retrieval
        vectorstore.similarity_search(
            job_description,
            k=3
        )

    except Exception:
        # continue even if embeddings fail
        pass

    # =========================
    # 🔥 SKILL MATCHING
    # =========================
    resume_skills = extract_skills(
        resume_text
    )

    job_skills = extract_skills(
        job_description
    )

    matched = sorted(list(
        set(resume_skills).intersection(
            set(job_skills)
        )
    ))

    missing = sorted(list(
        set(job_skills) - set(resume_skills)
    ))

    # =========================
    # 🔥 SCORE CALCULATION
    # =========================
    total_skills = len(job_skills)

    if total_skills > 0:

        score = round(
            (len(matched) / total_skills) * 100
        )

    else:

        score = 0

    # =========================
    # 🔥 VERDICT
    # =========================
    if score >= 75:

        verdict = "Strong match"

    elif score >= 50:

        verdict = "Good match"

    else:

        verdict = "Needs core skills"

    # =========================
    # 🔥 ROADMAP
    # =========================
    roadmap = {}

    if "django" in missing:

        roadmap["Django"] = [
            "Build CRUD APIs using Django REST Framework",
            "Connect PostgreSQL database",
            "Deploy Django app on Render"
        ]

    if "api" in missing:

        roadmap["API"] = [
            "Build REST APIs using FastAPI",
            "Test APIs using Postman",
            "Connect frontend with backend APIs"
        ]

    if "genai" in missing:

        roadmap["GenAI"] = [
            "Build AI agents using LLM APIs",
            "Learn embeddings and vector search",
            "Create RAG-based chatbot"
        ]

    if "openai" in missing:

        roadmap["OpenAI"] = [
            "Build chatbot using OpenAI API",
            "Practice prompt engineering",
            "Add conversation memory"
        ]

    # =========================
    # 🔥 PROFESSIONAL FEEDBACK
    # =========================
    professional_feedback = (
        f"You currently match "
        f"{len(matched)} out of "
        f"{len(job_skills)} required skills."
    )

    if missing:

        improvement_text = (
            "Focus on improving these skills: "
            + ", ".join(missing)
            + "."
        )

    else:

        improvement_text = (
            "Your profile strongly matches this role."
        )

    reasoning = f"""
Professional Feedback:
{professional_feedback}

Improvement Suggestions:
{improvement_text}
""".strip()

    # =========================
    # 🔥 RECOMMENDED PROJECT
    # =========================
    recommended_project = {
        "title": "AI-Powered eCommerce Returns Assistant",

        "stack": [
            "Django",
            "FastAPI",
            "LLM Chatbot"
        ],

        "features": [
            "Customer chat support",
            "Return automation",
            "AI response generation"
        ],

        "why": (
            "Matches the company's AI agents "
            "and eCommerce use-case."
        )
    }

    # =========================
    # 🔥 FINAL RESPONSE
    # =========================
    return {

        "score": score,

        "matched": matched,

        "missing": missing,

        "verdict": verdict,

        "roadmap": roadmap,

        "reasoning": reasoning,

        "project": recommended_project
    }