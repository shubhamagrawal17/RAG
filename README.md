# Final Local RAG Pipeline Setup Guide (Windows 11)

This guide will help you build a complete local RAG (Retrieval-Augmented Generation) pipeline using:

* Python 3.12
* VS Code
* Ollama
* LangChain
* ChromaDB
* Local Llama 3 Model

This setup works completely locally and free.

---

# STEP 1 — Install Python 3.12

Download:
[Python Downloads](https://www.python.org/downloads/windows/?utm_source=chatgpt.com)

During installation:

* ✅ Check `Add Python to PATH`
* ✅ Click `Disable path length limit`

Verify:

```cmd id="omc2r1"
python --version
pip --version
```

---

# STEP 2 — Install VS Code

Download:
[VS Code Download](https://code.visualstudio.com/Download?utm_source=chatgpt.com)

Install extensions:

* Python
* Pylance

---

# STEP 3 — Install Git

Download:
[Git Download](https://git-scm.com/download/win?utm_source=chatgpt.com)

Verify:

```cmd id="sok1tx"
git --version
```

---

# STEP 4 — Install Ollama

Download:
[Ollama Download](https://ollama.com/download/windows?utm_source=chatgpt.com)

After installation verify:

```cmd id="c3vpfm"
ollama list
```

---

# STEP 5 — Download Local LLM

Run:

```cmd id="yyt2vw"
ollama run llama3
```

This downloads the local Llama 3 model.

Verify:

```cmd id="ijjlwm"
ollama list
```

Expected:

```text id="vjlwm9"
llama3:latest
```
ollama pull nomic-embed-text

# llama3 = generates answers
# nomic-embed-text = creates high-quality embeddings for semantic search
---

# STEP 6 — Create Project Folder

Create folder:

```text id="wg5yxz"
C:\Projects\rag-project
```

Open folder in VS Code.

---

# STEP 7 — Open VS Code Terminal

Inside VS Code:

```text id="g88wqf"
Terminal → New Terminal
```

---

# STEP 8 — Create Virtual Environment

Run:

```cmd id="zjlwm3"
python -m venv venv
```

---

# STEP 9 — Activate Virtual Environment

## CMD

```cmd id="ovjlwm"
venv\Scripts\activate.bat
```

## PowerShell

If blocked:

Run PowerShell as Administrator:

```powershell id="uxs6qf"
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then activate:

```powershell id="b0q8ev"
.\venv\Scripts\Activate.ps1
```

Successful activation:

```text id="5ls6rf"
(venv)
```

---

# STEP 10 — Install Required Packages

Run:

```cmd id="k2t9bo"
pip install -U langchain langchain-community langchain-core langchain-ollama langchain-text-splitters chromadb pypdf
```

Then:

```cmd id="w9a1vu"
pip install unstructured
```

---

# STEP 11 — Create Project Structure

Create this structure:

```text id="ijjlwm"
rag-project
│
├── docs
│   └── myfile.pdf
│
├── app.py
└── venv
```

IMPORTANT:

* Do NOT manually create `chroma_db`
* ChromaDB manages it automatically

---

# STEP 12 — Add PDF

Place any PDF inside:

```text id="a2t8f3"
docs/
```

Example:

```text id="ww1ovg"
docs/myfile.pdf
```

---

# STEP 13 — Add Final Working RAG Code

Create:

```text id="h7t3mf"
app.py
```

Paste this FINAL code:

```python id="dr76tq"
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings, ChatOllama

# Load PDF
loader = PyPDFLoader("docs/myfile.pdf")
documents = loader.load()

# Split text into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=100
)

docs = text_splitter.split_documents(documents)

# Create embeddings
embeddings = OllamaEmbeddings(model="llama3")

# Create vector database
vectorstore = Chroma.from_documents(
    documents=docs,
    embedding=embeddings
)

# Create retriever
retriever = vectorstore.as_retriever()

# Load local LLM
llm = ChatOllama(model="llama3")

print("\nRAG Pipeline Ready!")

while True:
    query = input("\nAsk Question: ")

    if query.lower() == "exit":
        break

    # Retrieve relevant documents
    relevant_docs = retriever.invoke(query)

    # Combine retrieved content
    context = "\n\n".join([doc.page_content for doc in relevant_docs])

    # Create prompt
    prompt = f'''
    Answer the question based only on the context below.

    Context:
    {context}

    Question:
    {query}
    '''

    # Generate response
    response = llm.invoke(prompt)

    print("\nAnswer:")
    print(response.content)
```

---

# STEP 14 — Run the RAG Pipeline

Run:

```cmd id="b1z4vr"
python app.py
```

Expected output:

```text id="zjlwm7"
RAG Pipeline Ready!
```

---

# STEP 15 — Ask Questions

Examples:

```text id="sgt6wm"
What is this document about?
```

```text id="x0m8pf"
Summarize the PDF
```

```text id="l0c4dn"
What are the key points?
```

Exit:

```text id="u1y8ef"
exit
```

---

# RAG Architecture Flow

```text id="om1rzc"
PDF
→ Chunking
→ Embeddings
→ Vector Database
→ Retriever
→ LLM
→ AI Answer
```

---

# Important Concepts You Learned

## 1. Chunking

Splitting text into smaller pieces.

## 2. Embeddings

Converting text into vectors.

## 3. Vector Database

Stores vector embeddings.

## 4. Retriever

Finds relevant chunks.

## 5. LLM

Generates final response.

---

# Common Errors & Fixes

## PowerShell Activation Error

Fix:

```powershell id="m7n4qp"
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## ChromaDB Folder Error

Cause:

* manually creating `chroma_db`

Fix:

* delete the folder
* let ChromaDB manage it automatically

---

## LangChain Import Errors

Cause:

* latest package structure changes

Fix:

* use:

  * `langchain_ollama`
  * `langchain_text_splitters`

---

# Recommended Next Steps

After this works:

1. Multi-PDF RAG
2. Streamlit UI
3. Persistent ChromaDB
4. Azure OpenAI Integration
5. OpenAI API Integration
6. Conversation Memory
7. AI Agents
8. LangGraph
9. MCP
10. LLMOps

---

# Recommended Future Tools

* Docker Desktop
* Kubernetes
* FastAPI
* Streamlit
* Redis
* PostgreSQL
* OpenTelemetry
* LangGraph
* CrewAI

---

# Final Outcome

You now have:

* local LLM
* embeddings
* vector database
* semantic search
* document AI
* complete local RAG pipeline

