# =========================
# 🔥 LEARNING ROADMAP
# =========================
def generate_roadmap(missing_skills):

    roadmap_data = {

        "django": """
Django:
• Build CRUD APIs using Django REST Framework
• Connect PostgreSQL database
• Implement JWT authentication
• Deploy project on Render
""",

        "api": """
API:
• Build REST APIs using FastAPI
• Test APIs using Postman
• Connect frontend with backend APIs
• Learn request/response handling
""",

        "openai": """
OpenAI:
• Build chatbot using OpenAI API
• Practice prompt engineering
• Add conversation memory
• Create AI customer support bot
""",

        "genai": """
GenAI:
• Build AI agents using LLM APIs
• Learn embeddings and vector search
• Create RAG-based chatbot
• Explore AI agent workflows
""",

        "langchain": """
LangChain:
• Build RAG pipelines using LangChain
• Connect vector databases like FAISS or ChromaDB
• Implement memory and AI agents
• Build document Q&A chatbot
""",

        "postgres": """
PostgreSQL:
• Write SQL joins and aggregation queries
• Connect PostgreSQL with Django
• Design relational database schemas
• Optimize database queries
""",

        "postgresql": """
PostgreSQL:
• Write SQL joins and aggregation queries
• Connect PostgreSQL with Django
• Design relational database schemas
• Optimize database queries
"""
    }

    # =========================
    # 🔥 REMOVE DUPLICATES
    # =========================
    unique_skills = []

    for skill in missing_skills:

        skill = skill.lower().strip()

        if skill not in unique_skills:
            unique_skills.append(skill)

    # =========================
    # 🔥 BUILD ROADMAP
    # =========================
    final_roadmap = []

    for skill in unique_skills:

        if skill in roadmap_data:

            final_roadmap.append(
                roadmap_data[skill].strip()
            )

    # =========================
    # 🔥 FALLBACK
    # =========================
    if not final_roadmap:

        return """
No major skill gaps detected.

• Build more real-world AI + backend projects
• Deploy applications publicly
• Improve system design and API architecture
""".strip()

    return "\n\n".join(final_roadmap)