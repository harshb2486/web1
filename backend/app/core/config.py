from pydantic_settings import BaseSettings
from pydantic import Field
from typing import List


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://creatoros:creatoros_dev@localhost:5432/creatoros"
    REDIS_URL: str = "redis://localhost:6379/0"
    SECRET_KEY: str = "change-me-to-a-random-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    CORS_ORIGINS: List[str] = Field(default=["http://localhost:3000"])
    ENVIRONMENT: str = "development"

    APP_MODE: str = "demo"
    PROVIDER_MODE: str = "mock"

    YOUTUBE_API_KEY: str = ""
    REDDIT_CLIENT_ID: str = ""
    REDDIT_CLIENT_SECRET: str = ""
    NEWS_API_KEY: str = ""

    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4o-mini"

    VECTOR_PROVIDER: str = "memory"
    EMBEDDING_MODEL: str = "text-embedding-3-small"

    PIPELINE_ENABLED: bool = True
    PIPELINE_WORKER_CONCURRENCY: int = 3

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
