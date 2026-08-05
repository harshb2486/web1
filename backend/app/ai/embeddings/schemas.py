from typing import List, Optional
from pydantic import BaseModel


class EmbeddingRequest(BaseModel):
    text: str
    metadata: dict = {}


class EmbeddingResponse(BaseModel):
    id: str
    vector: List[float]
    dimension: int


class SearchRequest(BaseModel):
    query: str
    top_k: int = 5
    entity_type: Optional[str] = None


class UpsertRequest(BaseModel):
    id: str
    text: str
    metadata: dict = {}
