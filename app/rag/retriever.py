from app.config import settings
from app.rag.embedder import embed_query
from app.storage.vector_store import search_vectors


def retrieve_context(query: str, top_k: int | None = None) -> list[dict]:
    query_embedding = embed_query(query)
    return search_vectors(query_embedding, top_k=top_k or settings.top_k)

