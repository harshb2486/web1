from typing import List, Optional
from uuid import uuid4

from app.ai.embeddings.base import EmbeddingProvider, SearchResult
from app.ai.embeddings.factory import EmbeddingFactory


class EmbeddingService:
    def __init__(self, provider: EmbeddingProvider = None):
        self._provider = provider or EmbeddingFactory.get_provider()

    async def embed_text(self, text: str) -> List[float]:
        return await self._provider.embed(text)

    async def store_video(self, video_id: str, title: str, description: str = "") -> str:
        text = f"{title} {description}".strip()
        id_ = f"video_{video_id}"
        await self._provider.upsert(id_, text, {"entity_type": "video", "video_id": video_id})
        return id_

    async def store_recommendation(self, rec_id: str, topic: str, evidence: str = "") -> str:
        text = f"{topic} {evidence}".strip()
        id_ = f"rec_{rec_id}"
        await self._provider.upsert(id_, text, {"entity_type": "recommendation", "rec_id": rec_id})
        return id_

    async def store_topic(self, topic_id: str, topic: str, category: str = "") -> str:
        text = f"{topic} {category}".strip()
        id_ = f"topic_{topic_id}"
        await self._provider.upsert(id_, text, {"entity_type": "topic", "topic_id": topic_id})
        return id_

    async def store_memory(self, memory_id: str, category: str, key: str, value: str) -> str:
        text = f"{category} {key} {value}".strip()
        id_ = f"memory_{memory_id}"
        await self._provider.upsert(id_, text, {"entity_type": "memory", "memory_id": memory_id})
        return id_

    async def search(self, query: str, top_k: int = 5, entity_type: str = None) -> List[SearchResult]:
        return await self._provider.search(query, top_k, entity_type)

    async def search_videos(self, query: str, top_k: int = 5) -> List[SearchResult]:
        return await self.search(query, top_k, entity_type="video")

    async def search_recommendations(self, query: str, top_k: int = 5) -> List[SearchResult]:
        return await self.search(query, top_k, entity_type="recommendation")

    async def search_topics(self, query: str, top_k: int = 5) -> List[SearchResult]:
        return await self.search(query, top_k, entity_type="topic")

    async def delete(self, id: str) -> None:
        await self._provider.delete(id)

    async def health_check(self) -> bool:
        return await self._provider.health_check()
