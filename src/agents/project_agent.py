def generate_project_recommendation(missing, job_desc):
    jd = job_desc.lower()
    missing_set = set(missing)

    # =========================
    # 🎯 HIGH PRIORITY (JOB MATCH)
    # =========================
    if "ecommerce" in jd or "returns" in jd:
        return """
AI-Powered eCommerce Returns Assistant

Tech Stack:
• Django (backend)
• FastAPI (APIs)
• LLM chatbot

Features:
• Customer chat support
• Return automation
• AI response generation

Why:
Matches real company use-case (returns + AI agents)
"""

    # =========================
    # 🤖 LLM + LANGCHAIN PROJECT
    # =========================
    if "llm" in missing_set or "langchain" in missing_set:
        return """
🚀 Recommended Project:
AI Chatbot with Memory

Tech Stack:
• FastAPI
• LangChain
• LLM (OpenAI / Ollama)

Features:
• Context-aware responses
• Chat history memory
• Prompt engineering

Why:
Builds strong AI/LLM foundation
"""

    # =========================
    # ⚙️ BACKEND PROJECT
    # =========================
    if "django" in missing_set or "api" in missing_set:
        return """
🚀 Recommended Project:
Full Stack Backend System

Tech Stack:
• Django
• FastAPI
• PostgreSQL

Features:
• REST APIs
• CRUD operations
• Authentication system

Why:
Strengthens backend fundamentals
"""

    # =========================
    # 🔁 DEFAULT
    # =========================
    return """
🚀 Recommended Project:
Portfolio Full Stack App

Tech Stack:
• Django
• APIs
• Database

Features:
• End-to-end system
• Deployment
• Real-world use case

Why:
Covers all essential skills
"""