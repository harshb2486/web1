from app.core.config import settings
from app.ai.embeddings.base import EmbeddingProvider
from app.ai.embeddings.memory_provider import MemoryProvider


class EmbeddingFactory:
    _provider: EmbeddingProvider | None = None

    @classmethod
    def get_provider(cls) -> EmbeddingProvider:
        if cls._provider is None:
            cls._provider = cls._create_provider()
        return cls._provider

    @classmethod
    def _create_provider(cls) -> EmbeddingProvider:
        provider_name = getattr(settings, "VECTOR_PROVIDER", "memory")

        if provider_name == "memory":
            return MemoryProvider()
        else:
            raise ValueError(f"Unknown vector provider: {provider_name}")

    @classmethod
    def reset(cls) -> None:
        cls._provider = None
