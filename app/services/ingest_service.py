import shutil
from pathlib import Path

from fastapi import UploadFile

from app.config import settings
from app.rag.chunker import build_chunks
from app.rag.embedder import embed_texts
from app.rag.loader import load_document
from app.storage.vector_store import add_vectors, ensure_storage_paths


def save_upload(upload: UploadFile) -> Path:
    ensure_storage_paths()
    destination = settings.uploads_dir / upload.filename
    with destination.open("wb") as buffer:
        shutil.copyfileobj(upload.file, buffer)
    return destination


def ingest_document(upload: UploadFile) -> dict:
    if not upload.filename:
        raise ValueError("No file name provided.")

    extension = Path(upload.filename).suffix.lower()
    if extension not in {".pdf", ".txt"}:
        raise ValueError("Unsupported file type. Please upload a PDF or TXT file.")

    saved_path = save_upload(upload)
    document_pages = load_document(saved_path)
    chunks = build_chunks(
        document_pages=document_pages,
        file_name=upload.filename,
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
    )

    if not chunks:
        raise ValueError("No readable text found in the uploaded document.")

    vectors = embed_texts([item["text"] for item in chunks])
    add_vectors(vectors, chunks)

    return {
        "status": "success",
        "file_name": upload.filename,
        "chunks_indexed": len(chunks),
    }

