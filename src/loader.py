from langchain_community.document_loaders import PyPDFLoader
import tempfile

def load_pdf(uploaded_file):
     # Save uploaded file temporarily
     with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
          tmp.write(uploaded_file.read())
          file_path = tmp.name

     loader = PyPDFLoader(file_path)
     documents = loader.load()

     return documents