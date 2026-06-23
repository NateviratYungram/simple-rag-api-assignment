from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    openai_api_key: str = ""
    embedding_model: str = "text-embedding-3-small"
    chat_model: str = "gpt-4o-mini"
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

