import os
import time

from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings, ChatOllama

from prompt_template import prompt_template

# =========================================================
# CONFIGURATION
# =========================================================
DB_DIR = "chroma_db"
DOCS_DIR = "docs"

CHUNK_SIZE = 500
CHUNK_OVERLAP = 100

TOP_K = 5
FETCH_K = 10

SIMILARITY_THRESHOLD = 0.45

# =========================================================
# APPLICATION HEADER
# =========================================================
print("\n==================================================")
print("         ENTERPRISE LOCAL RAG PIPELINE")
print("==================================================")

# =========================================================
# LOAD EMBEDDING MODEL
# =========================================================
print("\n--> Loading embedding model...")

embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)

# =========================================================
# LOAD LOCAL LLM
# =========================================================
print("--> Loading local LLM...")

llm = ChatOllama(
    model="llama3",
    temperature=0.0
)

# =========================================================
# CHECK OLLAMA CONNECTION
# =========================================================
print("--> Verifying Ollama connection...")

try:

    llm.invoke("ping")

    print("--> Ollama connection successful")

except Exception:

    print("\nERROR: Ollama is not running.")
    print("Start Ollama first using:")
    print("ollama serve")

    exit()

# =========================================================
# VECTOR DATABASE
# =========================================================
collection_metadata = {
    "hnsw:space": "cosine"
}

if os.path.exists(DB_DIR) and os.listdir(DB_DIR):

    print(f"\n--> Existing vector database found at '{DB_DIR}'")

    vectorstore = Chroma(
        persist_directory=DB_DIR,
        embedding_function=embeddings,
        collection_metadata=collection_metadata
    )

    print("--> Vector database loaded successfully")

else:

    print("\n--> No existing vector database found")
    print("--> Starting ingestion pipeline...")

    if not os.path.exists(DOCS_DIR):

        os.makedirs(DOCS_DIR)

        raise FileNotFoundError(
            f"Created '{DOCS_DIR}' directory. "
            f"Please add PDF files and rerun."
        )

    pdf_files = [
        os.path.join(DOCS_DIR, file)
        for file in os.listdir(DOCS_DIR)
        if file.endswith(".pdf")
    ]

    if not pdf_files:

        raise FileNotFoundError(
            f"No PDF files found inside '{DOCS_DIR}'"
        )

    print(f"\n--> Found {len(pdf_files)} PDF file(s)")

    all_documents = []

    for index, pdf in enumerate(pdf_files):

        print(f"\n[{index + 1}/{len(pdf_files)}] Loading: {pdf}")

        try:

            loader = PyMuPDFLoader(pdf)

            documents = loader.load()

            for doc in documents:

                doc.metadata["source"] = os.path.basename(pdf)

            all_documents.extend(documents)

            print(f"--> Loaded {len(documents)} pages")

        except Exception as e:

            print(f"ERROR while loading {pdf}: {e}")

    print(f"\n--> Total loaded pages: {len(all_documents)}")

    # =====================================================
    # CHUNKING
    # =====================================================
    print("\n--> Splitting documents into chunks...")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )

    docs = splitter.split_documents(all_documents)

    print(f"--> Created {len(docs)} chunks")

    # =====================================================
    # VECTOR EMBEDDINGS
    # =====================================================
    print("\n--> Creating vector embeddings...")
    print("--> First run may take several minutes")

    start_time = time.time()

    vectorstore = Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        persist_directory=DB_DIR,
        collection_metadata=collection_metadata
    )

    total_ingestion_time = round(
        time.time() - start_time,
        2
    )

    print(
        f"\n--> Vector database created in "
        f"{total_ingestion_time} sec"
    )

# =========================================================
# APPLICATION READY
# =========================================================
print("\n==================================================")
print("               RAG PIPELINE READY")
print("==================================================")
print("Type 'exit' to quit")

# =========================================================
# MAIN QUERY LOOP
# =========================================================
while True:

    query = input("\nAsk Question: ").strip()

    if not query:
        continue

    if query.lower() == "exit":

        print("\nExiting application...")
        break

    print("\n--> Retrieving relevant context...")

    try:

        query_start_time = time.time()

        docs_and_scores = vectorstore.similarity_search_with_score(
            query,
            k=FETCH_K
        )

        print("\nRetrieved Scores:")

        for _, score in docs_and_scores:
            print(score)

        unique_docs = []

        seen_content = set()

        for doc, score in docs_and_scores:

            if score > SIMILARITY_THRESHOLD:
                continue

            if doc.page_content not in seen_content:

                doc.metadata["score"] = float(score)

                unique_docs.append(doc)

                seen_content.add(doc.page_content)

        unique_docs = unique_docs[:TOP_K]

        if not unique_docs:

            print("\n==================================================")
            print("                    ANSWER")
            print("==================================================\n")

            print(
                "I could not find relevant information "
                "in the documents."
            )

            continue

        # =================================================
        # DISPLAY SOURCES
        # =================================================
        print("\n==================================================")
        print("                    SOURCES")
        print("==================================================")

        for index, doc in enumerate(unique_docs):

            source = doc.metadata.get("source", "Unknown")

            page = doc.metadata.get("page", "N/A")

            score = round(
                doc.metadata.get("score", 0),
                4
            )

            print(f"""
Source {index + 1}
--------------------------------------------------
File       : {source}
Page       : {page + 1}
Score      : {score}

Preview:
{doc.page_content[:200]}
""")

        # =================================================
        # BUILD CONTEXT
        # =================================================
        context = "\n\n".join([
            doc.page_content
            for doc in unique_docs
        ])

        messages = prompt_template.format_messages(
            context=context,
            question=query
        )

        # =================================================
        # GENERATE RESPONSE
        # =================================================
        print("\n==================================================")
        print("                    ANSWER")
        print("==================================================\n")

        for chunk in llm.stream(messages):

            if chunk.content:

                print(
                    chunk.content,
                    end="",
                    flush=True
                )

        total_time = round(
            time.time() - query_start_time,
            2
        )

        print(f"\n\n--> Response generated in {total_time} sec")

    except Exception as e:

        print(f"\nERROR: {e}")