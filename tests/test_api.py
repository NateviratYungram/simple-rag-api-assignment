from fastapi.testclient import TestClient

from app.main import app


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
