from rest_framework.decorators import api_view
from rest_framework.response import Response

import sys
import os

# =========================
# 🔥 FIX PYTHON PATH
# =========================
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# Go to project root (career-copilot)
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "../../"))

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# =========================
# 🔥 IMPORT AI LOGIC (SAFE)
# =========================
try:
    # ✅ If you created file inside Django core/
    from core.langchain_agent import analyze_resume_with_langchain
except Exception:
    try:
        # ✅ If you moved it to src/
        from src.agents.langchain_agent import analyze_resume_with_langchain
    except Exception as e:
        analyze_resume_with_langchain = None
        print("❌ Import Error (LangChain Agent):", e)

# =========================
# 🔥 IMPORT LLM (SAFE)
# =========================
try:
    from src.llm import get_llm
except Exception as e:
    get_llm = None
    print("❌ Import Error (LLM):", e)


# =========================
# 🔥 API VIEW
# =========================
@api_view(['POST'])
def analyze_resume_api(request):
    try:
        resume_text = request.data.get("resume_text", "")
        job_description = request.data.get("job_description", "")

        # ❌ Safety checks
        if not analyze_resume_with_langchain:
            return Response(
                {"error": "LangChain agent not found"},
                status=500
            )

        # ✅ Load LLM safely
        llm = get_llm() if get_llm else None

        result = analyze_resume_with_langchain(
            resume_text,
            job_description,
            llm
        )

        return Response(result)

    except Exception as e:
        return Response({"error": str(e)}, status=500)