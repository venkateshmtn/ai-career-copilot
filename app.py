import re
import requests
import streamlit as st

from src.loader import load_pdf
from src.splitter import split_text
from src.embeddings import get_embeddings
from src.vectorstore import create_vectorstore
from src.llm import get_llm

from src.agents.roadmap_agent import generate_roadmap
from src.agents.project_agent import generate_project_recommendation
from src.agents.resume_agent import improve_resume
from src.agents.interview_agent import generate_interview_questions


# =========================
# 🔥 DJANGO BACKEND URL
# =========================
API_URL = "http://127.0.0.1:8000/analyze/"


# =========================
# 🔥 CACHE VECTORSTORE
# =========================
@st.cache_resource
def get_vectorstore(chunks):

    embeddings = get_embeddings()

    return create_vectorstore(
        chunks,
        embeddings
    )


# =========================
# 🔥 FORMAT SKILLS
# =========================
def format_skill(skill):

    mapping = {
        "llm": "LLM",
        "api": "API",
        "sql": "SQL",
        "git": "Git",
        "django": "Django",
        "postgres": "PostgreSQL",
        "langchain": "LangChain",
        "genai": "GenAI",
        "openai": "OpenAI",
        "faiss": "FAISS",
    }

    return mapping.get(
        skill.lower(),
        skill.title()
    )


# =========================
# 🔥 CLEAN ROADMAP
# =========================
def clean_roadmap(text):

    if not text:
        return ""

    cleaned = []

    for line in text.split("\n"):

        line = line.strip()

        if not line:
            continue

        # remove step numbering
        line = re.sub(
            r"Step\s*\d+:\s*",
            "",
            line,
            flags=re.IGNORECASE
        )

        # normalize bullets
        if line.startswith("-"):
            line = "•" + line[1:]

        # keep only headers + bullets
        if (
            line.endswith(":")
            or line.startswith("•")
        ):
            cleaned.append(line)

    # remove duplicates
    final = []

    for item in cleaned:

        if item not in final:
            final.append(item)

    return "\n".join(final)


# =========================
# 🔥 CLEAN INTERVIEW QUESTIONS
# =========================
def clean_interview_questions(text):

    if not text:
        return ""

    cleaned = []

    bad_phrases = [
        "technical questions",
        "behavioral questions",
        "project-based questions",
        "candidate resume",
        "job description",
        "here are",
    ]

    for line in text.split("\n"):

        line = line.strip()

        if not line:
            continue

        lower = line.lower()

        # remove garbage
        if any(
            bad in lower
            for bad in bad_phrases
        ):
            continue

        # normalize bullets
        if line.startswith("-"):
            line = "•" + line[1:]

        # keep only valid questions
        if (
            line.startswith("•")
            and line.endswith("?")
            and len(line.split()) >= 4
        ):
            cleaned.append(line)

    # remove duplicates
    final = []

    for q in cleaned:

        if q not in final:
            final.append(q)

    return "\n".join(final)


# =========================
# 🔥 FALLBACK QUESTIONS
# =========================
def fallback_questions():

    return """
• How would you build a REST API using Django?
• What is Django ORM and where have you used it?
• How would you integrate OpenAI into a chatbot?
• Explain how LangChain works in RAG applications?
• What are vector databases used for?
• Describe a project you built end-to-end?
• How do you debug API errors in backend systems?
• Explain prompt engineering with an example?
""".strip()


# =========================
# 🔥 UI
# =========================
st.set_page_config(
    page_title="AI Career Copilot",
    page_icon="📄",
    layout="wide"
)

st.title("📄 AI Career Copilot")

uploaded_file = st.file_uploader(
    "Upload Resume (PDF)",
    type="pdf"
)

job_desc = st.text_area(
    "Paste Job Description",
    height=250
)


# =========================
# 🔥 SESSION STATE
# =========================
if "analysis_done" not in st.session_state:
    st.session_state.analysis_done = False


# =========================
# 🔥 MAIN FLOW
# =========================
if uploaded_file:

    try:

        documents = load_pdf(uploaded_file)

        chunks = split_text(documents)

        full_resume = " ".join([
            doc.page_content
            for doc in documents
        ])

        vectorstore = get_vectorstore(
            tuple(chunks)
        )

        st.success("✅ Resume processed!")

    except Exception as e:

        st.error("⚠️ Resume processing failed")

        st.code(str(e))

        st.stop()

    # =========================
    # 🔥 ANALYZE MATCH
    # =========================
    if st.button("Analyze Match"):

        if not job_desc.strip():

            st.warning(
                "Please paste a job description."
            )

            st.stop()

        try:

            with st.spinner(
                "🔍 Analyzing profile..."
            ):

                response = requests.post(
                    API_URL,
                    json={
                        "resume_text": full_resume,
                        "job_description": job_desc
                    },
                    timeout=120
                )

            if response.status_code != 200:

                st.error(
                    f"Backend Error: {response.status_code}"
                )

                st.code(response.text)

                st.stop()

            data = response.json()

            st.session_state.analysis_done = True

            st.session_state.score = data.get(
                "score",
                0
            )

            st.session_state.matched = data.get(
                "matched",
                []
            )

            st.session_state.missing = data.get(
                "missing",
                []
            )

            st.session_state.reasoning = data.get(
                "reasoning",
                ""
            )

        except Exception as e:

            st.error("⚠️ Django backend not running")

            st.code(str(e))

            st.stop()

    # =========================
    # 🔥 SHOW RESULTS
    # =========================
    if st.session_state.analysis_done:

        score = st.session_state.score

        matched = (
            st.session_state.matched
            or ["None"]
        )

        missing = (
            st.session_state.missing
            or ["None"]
        )

        reasoning = st.session_state.reasoning

        real_missing = [
            s for s in missing
            if s != "None"
        ]

        # =========================
        # 🔥 VERDICT
        # =========================
        verdict = (
            "Strong fit"
            if score >= 75
            else "Good fit"
            if score >= 55
            else "Needs core skills"
        )

        st.write("## 🤖 Match Analysis")

        st.write(
            f"### Match Score: {score}%"
        )

        # =========================
        # 🔥 MATCHED
        # =========================
        st.write("### ✅ Matched Skills")

        for skill in matched:

            st.write(
                f"• {format_skill(skill)}"
            )

        # =========================
        # 🔥 MISSING
        # =========================
        st.write("### ❌ Missing Skills")

        for skill in missing:

            st.write(
                f"• {format_skill(skill)}"
            )

        # =========================
        # 🔥 VERDICT
        # =========================
        st.write("### 📌 Final Verdict")

        st.success(verdict)

        # =========================
        # 🔥 REASONING
        # =========================
        if reasoning:

            st.write("### 🧠 AI Reasoning")

            st.info(reasoning)

        # =========================
        # 🔥 ROADMAP
        # =========================
        if real_missing:

            roadmap = generate_roadmap(
                real_missing
            )

            roadmap = clean_roadmap(
                roadmap
            )

            st.write(
                "## 🚀 Learning Roadmap"
            )

            st.markdown(
                f"```\n{roadmap}\n```"
            )

        # =========================
        # 🔥 PROJECT
        # =========================
        if real_missing:

            project = (
                generate_project_recommendation(
                    real_missing,
                    job_desc
                )
            )

            st.write(
                "## 🚀 Recommended Project"
            )

            st.markdown(
                f"```\n{project.strip()}\n```"
            )

        # =========================
        # 🔥 INTERVIEW QUESTIONS
        # =========================
        if st.button(
            "🎯 Generate Interview Questions"
        ):

            llm = get_llm()

            with st.spinner(
                "🧠 Generating Questions..."
            ):

                raw_questions = (
                    generate_interview_questions(
                        llm,
                        full_resume,
                        job_desc
                    )
                )

            questions = (
                clean_interview_questions(
                    raw_questions
                )
            )

            if (
                not questions
                or questions.count("•") < 3
            ):

                questions = fallback_questions()

            st.write(
                "## 🎯 Interview Questions"
            )

            st.markdown(
                f"```\n{questions}\n```"
            )

    # =========================
    # 🔥 RESUME IMPROVER
    # =========================
    if (
        st.button("✨ Improve My Resume")
        and job_desc
    ):

        llm = get_llm()

        with st.spinner(
            "✍️ Improving Resume..."
        ):

            improved = improve_resume(
                llm,
                full_resume,
                job_desc
            )

        st.write("## ✨ Improved Resume")

        st.markdown(
            f"```\n{improved.strip()}\n```"
        )


# =========================
# 📌 FINAL TIP
# =========================
st.info(
    "💡 Build 2 strong projects (Django + API + LLM) to cross 75% 🚀"
)