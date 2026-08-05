from abc import ABC, abstractmethod
from typing import List, Optional
from pydantic import BaseModel


class SearchResult(BaseModel):
    id: str
    score: float
    text: str
    metadata: dict = {}


class EmbeddingProvider(ABC):
    @abstractmethod
    async def embed(self, text: str) -> List[float]:
        """Generate embedding vector for text."""

    @abstractmethod
    async def upsert(self, id: str, text: str, metadata: dict = None) -> None:
        """Store an embedding with metadata."""

    @abstractmethod
    async def search(self, query: str, top_k: int = 5, entity_type: str = None) -> List[SearchResult]:
        """Search for similar embeddings."""

    @abstractmethod
    async def delete(self, id: str) -> None:
        """Delete an embedding by ID."""

    @abstractmethod
    async def health_check(self) -> bool:
        """Check if the provider is healthy."""
