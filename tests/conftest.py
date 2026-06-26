from pathlib import Path

import pytest

from app.config import settings
from app.storage import vector_store


@pytest.fixture(autouse=True)
def isolate_storage(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    uploads_dir = tmp_path / "uploads"
    index_dir = tmp_path / "index"
    metadata_path = index_dir / "metadata.json"
    vectors_file = index_dir / "vectors.npy"

    monkeypatch.setattr(settings, "uploads_dir", uploads_dir)
    monkeypatch.setattr(settings, "index_dir", index_dir)
    monkeypatch.setattr(settings, "metadata_path", metadata_path)
    monkeypatch.setattr(vector_store, "VECTORS_FILE", vectors_file)

    vector_store.ensure_storage_paths()
