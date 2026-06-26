from google import genai

from app.config import settings


def get_gemini_client() -> genai.Client:
    if not settings.gemini_api_key:
        raise ValueError("GEMINI_API_KEY is not configured.")
    return genai.Client(api_key=settings.gemini_api_key)


def extract_embedding_values(embedding_item: object) -> list[float]:
    values = getattr(embedding_item, "values", None)
    if values is None and isinstance(embedding_item, dict):
        values = embedding_item.get("values")
    if values is None:
        raise ValueError("Gemini embedding response did not include vector values.")
    return [float(value) for value in values]


def embed_texts(texts: list[str]) -> list[list[float]]:
    client = get_gemini_client()
    vectors: list[list[float]] = []

    for text in texts:
        response = client.models.embed_content(
            model=settings.embedding_model,
            contents=text,
        )
        embeddings = getattr(response, "embeddings", None)
        if not embeddings:
            raise ValueError("Gemini embedding response was empty.")
        vectors.append(extract_embedding_values(embeddings[0]))

    return vectors


def embed_query(query: str) -> list[float]:
    return embed_texts([query])[0]
