# 🚀 AI Career Copilot

AI Career Copilot is an AI-powered resume analysis platform that helps candidates evaluate their resumes against job descriptions using Large Language Models (LLMs), Retrieval-Augmented Generation (RAG), LangChain, and semantic skill matching.

The system provides:
- ATS-style resume analysis
- Skill match scoring
- Missing skill detection
- Personalized learning roadmap
- AI-generated interview questions
- Resume improvement suggestions
- AI project recommendations

Built with Django REST Framework, Streamlit, LangChain, FAISS, and Hugging Face embeddings.

---

# ✨ Features

## 📄 Resume Analysis
- Upload PDF resume
- Extract and process resume text
- Compare resume against job description
- Calculate AI-based match score

## 🧠 AI Skill Matching
- Semantic skill extraction
- Skill normalization mapping
- Matched vs missing skills analysis
- Intelligent scoring system

## 🚀 Personalized Learning Roadmap
- Generates roadmap for missing skills
- Covers:
  - Django
  - APIs
  - OpenAI
  - LangChain
  - GenAI
  - PostgreSQL

## 🎯 AI Interview Question Generator
- Generates technical interview questions
- Role-specific AI-generated questions
- Backend + LLM focused preparation

## ✨ Resume Improver
- Improves resume summary
- Enhances project descriptions
- Optimizes technical skills section

## 🤖 AI Project Recommendation
- Suggests recruiter-relevant AI projects
- Personalized based on missing skills
- Focused on real-world AI applications

---

# 🛠️ Tech Stack

## Frontend
- Streamlit

## Backend
- Django
- Django REST Framework

## AI / NLP
- LangChain
- Hugging Face Transformers
- FAISS Vector Database
- Sentence Transformers
- RAG Pipeline

## Database / Processing
- PostgreSQL
- PDF Parsing
- Semantic Search

---

# 🧠 AI Concepts Used

- Retrieval-Augmented Generation (RAG)
- Embeddings
- Semantic Search
- Vector Databases
- Prompt Engineering
- Skill Normalization
- Resume Parsing
- NLP Pipelines

---

# 📂 Project Structure

```bash
career-copilot/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── django_backend/
│   ├── manage.py
│   ├── api/
│   ├── core/
│   └── django_backend/
│
├── src/
│   ├── agents/
│   ├── loader.py
│   ├── splitter.py
│   ├── embeddings.py
│   ├── vectorstore.py
│   └── llm.py
│
└── assets/
    └── screenshots/
```

---

# ⚙️ Installation

## 1️⃣ Clone Repository

```bash
git clone https://github.com/venkateshmtn/ai-career-copilot.git
cd ai-career-copilot
```

---

## 2️⃣ Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

#### Windows
```bash
venv\Scripts\activate
```

#### Mac/Linux
```bash
source venv/bin/activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Run Backend

```bash
cd django_backend
python manage.py runserver
```

Backend runs on:

```bash
http://127.0.0.1:8000
```

---

# ▶️ Run Frontend

Open a new terminal:

```bash
streamlit run app.py
```

Frontend runs on:

```bash
http://localhost:8501
```

---

# 📸 Screenshots

## 🏠 Home Page
![Home](assets/screenshots/home-page.png)

---

## 🤖 Match Analysis
![Match Analysis](assets/screenshots/match-analysis.png)

---

## 🚀 Learning Roadmap
![Roadmap](assets/screenshots/learning-roadmap.png)

---

## 💡 Recommended Project
![Project](assets/screenshots/recommended-project.png)

---

## 🎯 Interview Questions
![Interview Questions](assets/screenshots/interview-questions.png)

---

## ✨ Improved Resume
![Resume](assets/screenshots/improved-resume.png)

---

# 📈 Example Output

- Match Score Calculation
- Skill Gap Detection
- AI Career Roadmap
- AI Resume Optimization
- Technical Interview Preparation

---

# 🔥 Future Improvements

- JWT Authentication
- PostgreSQL Integration
- OpenAI/Gemini API Integration
- Multi-Resume Comparison
- Resume ATS Score Visualization
- Cloud Deployment (Render/Azure)

---

# 👨‍💻 Author

## Venkatesh Metan

- GitHub: https://github.com/venkateshmtn
- Portfolio: https://venkateshmtn.github.io/data-analyst-portfolio/
- LinkedIn: https://linkedin.com/in/venkateshmetan

---

# ⭐ If you found this project useful, give it a star!
