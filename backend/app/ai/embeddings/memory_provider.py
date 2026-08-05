import math
import hashlib
from typing import Dict, List, Optional

from app.ai.embeddings.base import EmbeddingProvider, SearchResult


class MemoryProvider(EmbeddingProvider):
    """In-memory embedding provider using hash-based pseudo-embeddings.

    Phase 3: Development/testing provider.
    Phase 4: Replace with pgvector/Qdrant/Pinecone.
    """

    def __init__(self):
        self._store: Dict[str, dict] = {}
        self._dimension = 384

    async def embed(self, text: str) -> List[float]:
        h = hashlib.sha256(text.encode()).digest()
        vec = []
        for i in range(self._dimension):
            byte_val = h[i % len(h)]
            sign = 1.0 if (i % 2 == 0) else -1.0
            vec.append(sign * (byte_val / 255.0))
        norm = math.sqrt(sum(v * v for v in vec))
        if norm > 0:
            vec = [v / norm for v in vec]
        return vec

    async def upsert(self, id: str, text: str, metadata: dict = None) -> None:
        vector = await self.embed(text)
        self._store[id] = {
            "text": text,
            "vector": vector,
            "metadata": metadata or {},
        }

    async def search(self, query: str, top_k: int = 5, entity_type: str = None) -> List[SearchResult]:
        query_vec = await self.embed(query)
        scores = []
        for id_, entry in self._store.items():
            if entity_type and entry["metadata"].get("entity_type") != entity_type:
                continue
            score = self._cosine_similarity(query_vec, entry["vector"])
            scores.append((id_, score, entry))
        scores.sort(key=lambda x: x[1], reverse=True)
        results = []
        for id_, score, entry in scores[:top_k]:
            results.append(SearchResult(
                id=id_,
                score=score,
                text=entry["text"],
                metadata=entry["metadata"],
            ))
        return results

    async def delete(self, id: str) -> None:
        self._store.pop(id, None)

    async def health_check(self) -> bool:
        return True

    def _cosine_similarity(self, a: List[float], b: List[float]) -> float:
        dot = sum(x * y for x, y in zip(a, b))
        norm_a = math.sqrt(sum(x * x for x in a))
        norm_b = math.sqrt(sum(x * x for x in b))
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return dot / (norm_a * norm_b)

    @property
    def size(self) -> int:
        return len(self._store)
