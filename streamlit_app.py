import os
import time
import streamlit as st

from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings, ChatOllama

from prompt_template import prompt_template

# =========================================================
# PAGE CONFIGURATION
# =========================================================
st.set_page_config(
    page_title="Enterprise Local RAG Assistant",
    page_icon="🤖",
    layout="wide"
)

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
# HEADER
# =========================================================
st.title("🚀 Enterprise Local RAG Assistant")

st.caption(
    "Private AI Knowledge Assistant powered by "
    "Ollama + LangChain + ChromaDB"
)

# =========================================================
# SIDEBAR
# =========================================================
with st.sidebar:

    st.header("⚙️ System Configuration")

    st.code(f"""
Model                 : llama3
Embedding Model       : nomic-embed-text

Chunk Size            : {CHUNK_SIZE}
Chunk Overlap         : {CHUNK_OVERLAP}

Top K                 : {TOP_K}
Fetch K               : {FETCH_K}

Similarity Threshold  : {SIMILARITY_THRESHOLD}
""")

# =========================================================
# INITIALIZE PIPELINE
# =========================================================
@st.cache_resource
def initialize_pipeline():

    embeddings = OllamaEmbeddings(
        model="nomic-embed-text"
    )

    llm = ChatOllama(
        model="llama3",
        temperature=0.0
    )

    collection_metadata = {
        "hnsw:space": "cosine"
    }

    if os.path.exists(DB_DIR) and os.listdir(DB_DIR):

        vectorstore = Chroma(
            persist_directory=DB_DIR,
            embedding_function=embeddings,
            collection_metadata=collection_metadata
        )

    else:

        st.info(
            "Building vector database for the first time..."
        )

        pdf_files = [
            os.path.join(DOCS_DIR, file)
            for file in os.listdir(DOCS_DIR)
            if file.endswith(".pdf")
        ]

        all_documents = []

        for pdf in pdf_files:

            loader = PyMuPDFLoader(pdf)

            documents = loader.load()

            for doc in documents:

                doc.metadata["source"] = os.path.basename(pdf)

            all_documents.extend(documents)

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP
        )

        docs = splitter.split_documents(all_documents)

        vectorstore = Chroma.from_documents(
            documents=docs,
            embedding=embeddings,
            persist_directory=DB_DIR,
            collection_metadata=collection_metadata
        )

    return vectorstore, llm

vectorstore, llm = initialize_pipeline()

# =========================================================
# SESSION STATE
# =========================================================
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "retrieved_docs" not in st.session_state:
    st.session_state.retrieved_docs = []

# =========================================================
# MAIN LAYOUT
# =========================================================
chat_col, source_col = st.columns([2, 1])

# =========================================================
# CHAT HISTORY
# =========================================================
with chat_col:

    for message in st.session_state.chat_history:

        with st.chat_message(message["role"]):

            st.markdown(message["content"])

# =========================================================
# USER INPUT
# =========================================================
user_query = st.chat_input(
    "Ask questions about your documents..."
)

# =========================================================
# PROCESS QUERY
# =========================================================
if user_query:

    with chat_col:

        with st.chat_message("user"):

            st.markdown(user_query)

    st.session_state.chat_history.append({
        "role": "user",
        "content": user_query
    })

    with chat_col:

        with st.chat_message("assistant"):

            response_placeholder = st.empty()

            try:

                start_time = time.time()

                docs_and_scores = vectorstore.similarity_search_with_score(
                    user_query,
                    k=FETCH_K
                )

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

                st.session_state.retrieved_docs = unique_docs

                # =================================================
                # NO RELEVANT CONTEXT
                # =================================================
                if not unique_docs:

                    final_response = (
                        "I could not find relevant "
                        "information in the documents."
                    )

                    response_placeholder.markdown(
                        final_response
                    )

                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": final_response
                    })

                else:

                    context = "\n\n".join([
                        doc.page_content
                        for doc in unique_docs
                    ])

                    messages = prompt_template.format_messages(
                        context=context,
                        question=user_query
                    )

                    full_response = ""

                    for chunk in llm.stream(messages):

                        if chunk.content:

                            full_response += chunk.content

                            response_placeholder.markdown(
                                full_response + "▌"
                            )

                    response_placeholder.markdown(
                        full_response
                    )

                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": full_response
                    })

                total_time = round(
                    time.time() - start_time,
                    2
                )

                st.caption(
                    f"⚡ Response generated in "
                    f"{total_time} sec"
                )

            except Exception as e:

                st.error(f"🚨 Inference Error: {e}")

# =========================================================
# SOURCE PANEL
# =========================================================
with source_col:

    st.subheader("📚 Retrieved Sources")

    if st.session_state.retrieved_docs:

        for index, doc in enumerate(
            st.session_state.retrieved_docs
        ):

            source = doc.metadata.get(
                "source",
                "Unknown"
            )

            page = doc.metadata.get(
                "page",
                0
            )

            score = round(
                doc.metadata.get("score", 0),
                4
            )

            with st.expander(
                f"Source {index + 1} | "
                f"{source} | Page {page + 1}"
            ):

                st.markdown(
                    f"**Similarity Score:** `{score}`"
                )

                st.code(doc.page_content)

    else:

        st.info(
            "Submit a query to inspect retrieved chunks."
        )