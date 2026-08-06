import os
from pathlib import Path

from pydantic_settings import BaseSettings
from pydantic import Field
from typing import List


BASE_DIR = Path(__file__).resolve().parent.parent.parent


def _default_database_url() -> str:
    if os.environ.get("DATABASE_URL"):
        return os.environ["DATABASE_URL"]
    sqlite_path = BASE_DIR / "db.sqlite3"
    return f"sqlite+aiosqlite:///{sqlite_path}"


class Settings(BaseSettings):
    DATABASE_URL: str = _default_database_url()
    REDIS_URL: str = "redis://localhost:6379/0"
    SECRET_KEY: str = "dev-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    CORS_ORIGINS: List[str] = Field(default=["http://localhost:3000"])
    ENVIRONMENT: str = "development"

    APP_MODE: str = "demo"
    PROVIDER_MODE: str = "mock"

    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4o-mini"
    YOUTUBE_API_KEY: str = ""
    REDDIT_CLIENT_ID: str = ""
    REDDIT_CLIENT_SECRET: str = ""
    NEWS_API_KEY: str = ""

    VECTOR_PROVIDER: str = "memory"
    EMBEDDING_MODEL: str = "text-embedding-3-small"

    PIPELINE_ENABLED: bool = True
    PIPELINE_WORKER_CONCURRENCY: int = 3

    @property
    def is_sqlite(self) -> bool:
        return "sqlite" in self.DATABASE_URL

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
