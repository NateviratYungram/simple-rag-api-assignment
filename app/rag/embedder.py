from openai import OpenAI

from app.config import settings


def get_openai_client() -> OpenAI:
    if not settings.openai_api_key:
        raise ValueError("OPENAI_API_KEY is not configured.")
    return OpenAI(api_key=settings.openai_api_key)


def embed_texts(texts: list[str]) -> list[list[float]]:
    client = get_openai_client()
    response = client.embeddings.create(model=settings.embedding_model, input=texts)
    return [item.embedding for item in response.data]


def embed_query(query: str) -> list[float]:
    return embed_texts([query])[0]

