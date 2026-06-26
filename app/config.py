from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    gemini_api_key: str = ""
    embedding_model: str = "gemini-embedding-001"
    chat_model: str = "gemini-2.5-flash"
    chunk_size: int = 800
    chunk_overlap: int = 150
    top_k: int = 4
    uploads_dir: Path = BASE_DIR / "data" / "uploads"
    index_dir: Path = BASE_DIR / "data" / "index"
    metadata_path: Path = BASE_DIR / "data" / "index" / "metadata.json"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
