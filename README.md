# 🚀 Enterprise Local RAG Pipeline

A fully local **Enterprise-Grade Retrieval-Augmented Generation (RAG)** system powered by:

* Ollama
* LangChain
* ChromaDB
* Streamlit
* Llama 3
* Nomic Embeddings

This project allows you to:

✅ Chat with your PDFs locally
✅ Run AI completely offline
✅ Build a private enterprise knowledge assistant
✅ Perform semantic search over documents
✅ Create a production-style RAG architecture

---

# 📌 Features

* Fully Local AI (No OpenAI API Required)
* PDF Document Ingestion
* Semantic Search with Vector Embeddings
* ChromaDB Vector Storage
* Enterprise Prompt Guardrails
* Hallucination Reduction
* Streaming AI Responses
* Streamlit Chat UI
* Multi-PDF Support
* Source Transparency
* Similarity Score Filtering

---

# 🏗️ Architecture

```text
PDF Documents
      ↓
PyMuPDFLoader
      ↓
Text Chunking
      ↓
Embeddings (nomic-embed-text)
      ↓
ChromaDB Vector Store
      ↓
Similarity Search
      ↓
Context Filtering
      ↓
Llama 3
      ↓
Grounded AI Response
```

---

# 🛠️ Tech Stack

| Component  | Technology       |
| ---------- | ---------------- |
| LLM        | Llama 3          |
| Embeddings | nomic-embed-text |
| Framework  | LangChain        |
| Vector DB  | ChromaDB         |
| UI         | Streamlit        |
| Runtime    | Ollama           |
| Language   | Python 3.12      |

---

# 📂 Project Structure

```text
rag-project/
│
├── docs/
│   └── your-pdf-files.pdf
│
├── chroma_db/
│
├── app.py
├── streamlit_app.py
├── prompt_template.py
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

# ⚙️ Prerequisites

Before starting, install:

* Python 3.12
* VS Code
* Git
* Ollama

---

# STEP 1 — Install Python 3.12

Download Python:

[https://www.python.org/downloads/windows/](https://www.python.org/downloads/windows/)

During installation:

✅ Check `Add Python to PATH`
✅ Click `Disable path length limit`

Verify:

```bash
python --version
pip --version
```

---

# STEP 2 — Install VS Code

Download:

[https://code.visualstudio.com/](https://code.visualstudio.com/)

Recommended Extensions:

* Python
* Pylance

---

# STEP 3 — Install Git

Download:

[https://git-scm.com/download/win](https://git-scm.com/download/win)

Verify:

```bash
git --version
```

---

# STEP 4 — Install Ollama

Download:

[https://ollama.com/download/windows](https://ollama.com/download/windows)

Verify installation:

```bash
ollama --version
```

---

# STEP 5 — Download AI Models

Download Llama 3:

```bash
ollama run llama3
```

Download embedding model:

```bash
ollama pull nomic-embed-text
```

Verify models:

```bash
ollama list
```

Expected output:

```text
llama3
nomic-embed-text
```

---

# STEP 6 — Create Project Folder

```text
C:\Projects\rag-project
```

Open this folder in VS Code.

---

# STEP 7 — Create Virtual Environment

Open terminal inside VS Code:

```bash
python -m venv venv
```

---

# STEP 8 — Activate Virtual Environment

## CMD

```bash
venv\Scripts\activate.bat
```

## PowerShell

If blocked:

```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then:

```powershell
.\venv\Scripts\Activate.ps1
```

Successful activation:

```text
(venv)
```

---

# STEP 9 — Install Dependencies

Create:

```text
requirements.txt
```

Install packages:

```bash
pip install -r requirements.txt
```

---

# STEP 10 — Add PDF Documents

Place your PDFs inside:

```text
docs/
```

Example:

```text
docs/kubernetes-guide.pdf
docs/devops-notes.pdf
```

---

# STEP 11 — Run CLI RAG Application

```bash
python app.py
```

Expected:

```text
RAG PIPELINE READY
```

Ask questions:

```text
What is Kubernetes?
Explain ingress controller
What is CI/CD?
```

Exit:

```text
exit
```

---

# STEP 12 — Run Streamlit UI

```bash
streamlit run streamlit_app.py
```

Browser opens automatically.

Features:

* Chat interface
* Source inspection
* Similarity scores
* Streaming responses

---

# 🧠 How This RAG System Works

## 1. Document Loading

PDFs are loaded using:

```python
PyMuPDFLoader
```

Why?

* Faster than PyPDF
* Better table extraction
* Better enterprise document parsing

---

## 2. Chunking

Large documents are split into smaller chunks.

Example:

```python
CHUNK_SIZE = 500
CHUNK_OVERLAP = 100
```

This improves retrieval quality.

---

## 3. Embeddings

Text chunks are converted into vectors using:

```text
nomic-embed-text
```

Embeddings allow semantic similarity search.

---

## 4. Vector Database

Embeddings are stored inside:

```text
ChromaDB
```

This enables fast retrieval.

---

## 5. Similarity Search

User query is converted into embeddings.

Closest chunks are retrieved using vector similarity.

---

## 6. Grounded AI Response

Retrieved context is sent to:

```text
llama3
```

The AI responds ONLY from retrieved documents.

---

# 🛡️ Hallucination Prevention

This project uses multiple enterprise guardrails:

* Similarity Threshold Filtering
* Strict Prompt Engineering
* Context Validation
* Duplicate Removal
* Retrieval Filtering

Example:

```python
SIMILARITY_THRESHOLD = 0.45
```

Lower score = better semantic match.

---

# 📊 Recommended Settings

```python
CHUNK_SIZE = 500
CHUNK_OVERLAP = 100

TOP_K = 5
FETCH_K = 10

SIMILARITY_THRESHOLD = 0.45
```

---

# 🔥 First Run Behavior

First run may take several minutes because:

* PDFs are loaded
* Text is chunked
* Embeddings are generated
* Vector DB is created

Subsequent runs are much faster because:

```text
chroma_db/
```

is reused.

---

# 🧹 Rebuild Vector Database

If you:

* change chunk size
* switch embedding models
* modify retrieval logic

Delete:

```text
chroma_db/
```

Then rerun the application.

---

# 🚨 Common Errors & Fixes

---

## Ollama Not Running

Error:

```text
Connection refused
```

Fix:

```bash
ollama serve
```

---

## No PDF Files Found

Fix:

Place PDFs inside:

```text
docs/
```

---

## PowerShell Activation Error

Fix:

```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## ChromaDB Issues

Fix:

Delete:

```text
chroma_db/
```

Then rerun ingestion.

---

# 📈 Future Improvements

Possible upgrades:

* Hybrid Search (BM25 + Vector Search)
* Reranking Models
* Multi-Modal RAG
* Conversational Memory
* Metadata Filtering
* API Deployment
* Docker Support
* Kubernetes Deployment
* Authentication Layer
* Multi-User Chat

---

# 🎯 Recommended Use Cases

* Enterprise Knowledge Base
* DevOps Documentation Assistant
* Kubernetes Assistant
* Internal Company Search
* Compliance Documentation
* Technical PDF Search
* AI Helpdesk
* Cloud Architecture Assistant

---

# 📚 Recommended Learning Topics

To improve this project further, learn:

* Vector Databases
* Embeddings
* LangChain
* Prompt Engineering
* ChromaDB
* RAG Architecture
* LLM Fine-Tuning
* Kubernetes AI Workloads

---

# 🤝 Contributing

Feel free to fork this repository and improve it.

Possible contributions:

* Better UI
* Faster retrieval
* Better ranking
* New loaders
* Cloud deployment support

---

# 📜 License

This project is for educational and learning purposes.

---

# ⭐ Final Notes

This project demonstrates how modern enterprise AI systems work using:

* Retrieval-Augmented Generation (RAG)
* Semantic Search
* Local LLMs
* Vector Databases

Everything runs fully locally and privately without external APIs.

Perfect for:

* learning AI engineering
* enterprise AI demos
* DevOps AI assistants
* private document chat systems
