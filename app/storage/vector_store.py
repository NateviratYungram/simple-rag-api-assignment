import json

import numpy as np

from app.config import settings


VECTORS_FILE = settings.index_dir / "vectors.npy"


def ensure_storage_paths() -> None:
    settings.uploads_dir.mkdir(parents=True, exist_ok=True)
    settings.index_dir.mkdir(parents=True, exist_ok=True)


def load_metadata() -> list[dict]:
    ensure_storage_paths()
    if not settings.metadata_path.exists():
        return []
    return json.loads(settings.metadata_path.read_text(encoding="utf-8"))


def save_metadata(metadata: list[dict]) -> None:
    ensure_storage_paths()
    settings.metadata_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")


def load_vectors() -> np.ndarray | None:
    ensure_storage_paths()
    if not VECTORS_FILE.exists():
        return None
    return np.load(VECTORS_FILE)


def save_vectors(vectors: np.ndarray) -> None:
    ensure_storage_paths()
    np.save(VECTORS_FILE, vectors)


def add_vectors(vectors: list[list[float]], metadata_items: list[dict]) -> None:
    if not vectors:
        return

    ensure_storage_paths()
    array = np.array(vectors, dtype="float32")
    existing_vectors = load_vectors()
    if existing_vectors is None:
        combined_vectors = array
    else:
        combined_vectors = np.vstack([existing_vectors, array])

    save_vectors(combined_vectors)

    metadata = load_metadata()
    metadata.extend(metadata_items)
    save_metadata(metadata)


def search_vectors(query_vector: list[float], top_k: int) -> list[dict]:
    vectors = load_vectors()
    metadata = load_metadata()

    if vectors is None or len(vectors) == 0 or not metadata:
        return []

    query_array = np.array(query_vector, dtype="float32")
    distances = np.linalg.norm(vectors - query_array, axis=1)
    ranked_indices = np.argsort(distances)[:top_k]

    results: list[dict] = []
    for idx in ranked_indices:
        if idx >= len(metadata):
            continue
        item = dict(metadata[idx])
        item["score"] = float(distances[idx])
        results.append(item)
    return results


def has_indexed_documents() -> bool:
    vectors = load_vectors()
    return bool(vectors is not None and len(vectors) > 0)
