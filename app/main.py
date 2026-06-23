from fastapi import FastAPI

from app.api.routes import router
from app.storage.vector_store import ensure_storage_paths


ensure_storage_paths()

app = FastAPI(title="Simple RAG API", version="0.1.0")
app.include_router(router)

