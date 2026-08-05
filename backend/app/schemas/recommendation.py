from pydantic import BaseModel
from typing import List, Optional


class RecommendationResponse(BaseModel):
    id: str
    topic: str
    confidence: int
    evidence: List[str]
    expectedViews: dict
    expectedRevenue: dict
    risks: List[str]
    similarContent: dict
    publishTime: str
    category: str
    potential: str
