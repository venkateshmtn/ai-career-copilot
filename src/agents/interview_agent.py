import re


# =========================
# 🔥 CLEAN QUESTION
# =========================
def clean_question(line):

    line = line.strip()

    # remove numbering
    line = re.sub(r"^\d+[\).\-\s]*", "", line)

    # normalize bullets
    if line.startswith("-"):
        line = "•" + line[1:]

    # add bullet if missing
    if not line.startswith("•"):
        line = "• " + line.replace("•", "").strip()

    return line.strip()


# =========================
# 🔥 INTERVIEW QUESTION GENERATOR
# =========================
def generate_interview_questions(
    llm,
    resume_text,
    job_desc
):

    prompt = f"""
You are a senior technical interviewer.

Generate realistic technical interview questions
for a software developer candidate.

Resume:
{resume_text}

Job Description:
{job_desc}

STRICT RULES:
- Output ONLY interview questions
- Every line MUST end with '?'
- No explanations
- No summaries
- No headings
- No skill statements
- No repeated questions
- Maximum 8 questions
- Use bullet points only

GOOD EXAMPLES:
• How would you build a REST API using Django?
• What is LangChain memory?
• How do vector databases work?
• Explain a project you built end-to-end?
"""

    try:

        response = llm.invoke(prompt)

        # =========================
        # 🔥 HANDLE STRING / OBJECT
        # =========================
        if hasattr(response, "content"):
            result = response.content.strip()
        else:
            result = str(response).strip()

        # =========================
        # 🔥 CLEANING
        # =========================
        cleaned = []

        bad_patterns = [
            "summary",
            "skills",
            "requirements",
            "job description",
            "candidate",
            "responsibilities",
            "experience in",
            "knowledge of"
        ]

        for line in result.split("\n"):

            line = clean_question(line)

            lower = line.lower()

            # skip empty
            if not line:
                continue

            # skip hallucinated sections
            if any(
                bad in lower
                for bad in bad_patterns
            ):
                continue

            # keep only questions
            if not line.endswith("?"):
                continue

            # avoid huge lines
            if len(line.split()) > 20:
                continue

            cleaned.append(line)

        # =========================
        # 🔥 REMOVE DUPLICATES
        # =========================
        final = []

        for question in cleaned:

            if question not in final:
                final.append(question)

        # =========================
        # 🔥 LIMIT TO 8
        # =========================
        final = final[:8]

        # =========================
        # 🔥 FALLBACK SAFETY
        # =========================
        if len(final) < 3:
            return fallback_questions()

        return "\n".join(final)

    except Exception:

        return fallback_questions()


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