from io import BytesIO

from fastapi.testclient import TestClient

from app.main import app
from app.services import ingest_service, query_service


client = TestClient(app)


def test_health_check() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_ask_requires_query() -> None:
    response = client.post("/ask", json={"query": ""})

    assert response.status_code == 422


def test_ingest_rejects_unsupported_file_type() -> None:
    response = client.post(
        "/ingest",
        files={"file": ("notes.docx", b"dummy content", "application/octet-stream")},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Unsupported file type. Please upload a PDF or TXT file."


def test_ask_rejects_when_no_documents_are_indexed() -> None:
    response = client.post("/ask", json={"query": "What is this document about?"})

    assert response.status_code == 400
    assert response.json()["detail"] == "No indexed documents found. Please upload a document first."


def test_ingest_and_ask_returns_grounded_sources(monkeypatch) -> None:
    def fake_embed_texts(texts: list[str]) -> list[list[float]]:
        return [[0.1, 0.2, 0.3] for _ in texts]

    def fake_generate_answer(query: str, context_chunks: list[dict]) -> str:
        assert query == "What does the document say?"
        assert len(context_chunks) == 1
        assert context_chunks[0]["file_name"] == "sample.txt"
        return "The document says Codex builds a simple RAG API."

    monkeypatch.setattr(ingest_service, "embed_texts", fake_embed_texts)
    monkeypatch.setattr(query_service, "generate_answer", fake_generate_answer)
    monkeypatch.setattr(
        query_service,
        "retrieve_context",
        lambda query: [
            {
                "file_name": "sample.txt",
                "page": None,
                "text": "Codex builds a simple RAG API.",
                "score": 0.0,
            }
        ],
    )

    ingest_response = client.post(
        "/ingest",
        files={"file": ("sample.txt", BytesIO(b"Codex builds a simple RAG API."), "text/plain")},
    )

    assert ingest_response.status_code == 200
    assert ingest_response.json()["status"] == "success"
    assert ingest_response.json()["chunks_indexed"] == 1

    ask_response = client.post("/ask", json={"query": "What does the document say?"})

    assert ask_response.status_code == 200
    payload = ask_response.json()
    assert payload["answer"] == "The document says Codex builds a simple RAG API."
    assert len(payload["sources"]) == 1
    assert payload["sources"][0]["file_name"] == "sample.txt"
    assert payload["sources"][0]["text"] == "Codex builds a simple RAG API."
