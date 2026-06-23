from app.rag.generator import generate_answer
from app.rag.retriever import retrieve_context
from app.storage.vector_store import has_indexed_documents


def answer_query(query: str) -> dict:
    if not has_indexed_documents():
        raise ValueError("No indexed documents found. Please upload a document first.")

    context_chunks = retrieve_context(query)
    if not context_chunks:
        return {
            "answer": "No relevant information was found in the document.",
            "sources": [],
        }

    answer = generate_answer(query, context_chunks)
    return {
        "answer": answer,
        "sources": context_chunks,
    }

