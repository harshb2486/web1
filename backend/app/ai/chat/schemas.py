from pydantic import BaseModel
from typing import Optional, List


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str
    intent: str
    confidence: float
    sources_used: List[str] = []


class ChatHistoryEntry(BaseModel):
    id: str
    role: str
    content: str
    intent: Optional[str] = None
    created_at: Optional[str] = None
