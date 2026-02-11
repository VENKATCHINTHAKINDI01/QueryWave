from typing import Dict, Any

from app.exceptions import RoutingException
from app.utils.logger import get_logger

from app.orchestration.context_builder import build_context
from app.pipelines.document_rag.loader import load_documents
from app.pipelines.document_rag.chunker import chunk_documents
from app.pipelines.document_rag.retriever import DocumentRetriever
from app.llm.embeddings import load_embedding_model
from app.llm.model_loader import load_llm
from app.llm.response_generator import generate_response
from app.pipelines.arxiv_rag.arxiv_fetcher import fetch_arxiv_pdf
from app.pipelines.document_rag.chunker import chunk_documents
from app.pipelines.document_rag.retriever import DocumentRetriever


logger = get_logger(__name__)

# ✅ Load models ONCE (singleton style)
embedding_model = load_embedding_model(
    "sentence-transformers/all-MiniLM-L6-v2"
)

llm = load_llm("llama3")


def execute_tool(routing_payload: Dict[str, Any]) -> Dict[str, Any]:

    mode = routing_payload.get("mode")
    query = routing_payload.get("query")

    logger.info(f"Executing tool for mode: {mode}")

    if mode == "document":
        return _execute_document_pipeline(query, routing_payload)

    if mode == "web":
        return _execute_web_pipeline(query, routing_payload)

    if mode == "arxiv":
        return _execute_arxiv_pipeline(query, routing_payload)

    raise RoutingException(
        message=f"No tool execution defined for mode: {mode}",
        error_code="TOOL_NOT_FOUND"
    )


# -----------------------------
# Document Pipeline
# -----------------------------

def _execute_document_pipeline(query: str, payload: Dict) -> Dict[str, Any]:

    state = payload.get("state", {})
    uploaded_files = state.get("uploaded_files", [])

    if "document_retriever" not in state:

        logger.info("Initializing retriever for first time")

        documents = load_documents(uploaded_files)
        chunks = chunk_documents(documents)

        retriever = DocumentRetriever(embedding_model)
        retriever.index_chunks(chunks)

        state["document_retriever"] = retriever

    retriever = state["document_retriever"]

    retrieved_chunks = retriever.retrieve(query, top_k=5)

    context = build_context(
        user_query=query,
        chat_history=state.get("chat_history", []),
        retrieval_data={
            "source": "documents",
            "chunks": retrieved_chunks
        }
    )

    final_answer = generate_response(llm, context)

    return {
        "status": "success",
        "data": {
        "answer": final_answer,
        "sources": retrieved_chunks
    }
    }

# -----------------------------
# Web Pipeline (placeholder)
# -----------------------------

def _execute_web_pipeline(query: str, payload: Dict) -> Dict[str, Any]:

    context = build_context(
        user_query=query,
        chat_history=payload.get("state", {}).get("chat_history", []),
        retrieval_data={
            "source": "web",
            "note": "Web search integration coming next"
        }
    )

    final_answer = generate_response(llm, context)

    return {
        
    "status": "success",
    "data": {
        "answer": final_answer,
        "sources": []
        }
    }


# -----------------------------
# arXiv Pipeline (placeholder)
# -----------------------------


def _execute_arxiv_pipeline(query: str, payload: Dict) -> Dict[str, Any]:

    state = payload.get("state", {})

    arxiv_id = state.get("arxiv_id")

    if not arxiv_id:
        raise RoutingException(
            message="No arXiv ID provided",
            error_code="ARXIV_ID_MISSING"
        )

    # Cache per paper
    cache_key = f"arxiv_retriever_{arxiv_id}"

    if cache_key not in state:

        logger.info(f"Initializing retriever for arXiv paper {arxiv_id}")

        paper_text = fetch_arxiv_pdf(arxiv_id)

        documents = [{"source": arxiv_id, "text": paper_text}]
        chunks = chunk_documents(documents)

        retriever = DocumentRetriever(embedding_model)
        retriever.index_chunks(chunks)

        state[cache_key] = retriever

    retriever = state[cache_key]

    retrieved_chunks = retriever.retrieve(query, top_k=5)

    context = build_context(
        user_query=query,
        chat_history=state.get("chat_history", []),
        retrieval_data={
            "source": "arxiv",
            "chunks": retrieved_chunks
        }
    )

    final_answer = generate_response(llm, context)

    return {
        "status": "success",
        "data": {
            "answer": final_answer,
            "sources": retrieved_chunks
        }
    }
