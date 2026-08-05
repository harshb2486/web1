from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import datetime


class MemoryEntry(BaseModel):
    id: str
    category: str
    key: str
    value: dict
    confidence: float
    updated_at: Optional[datetime] = None


class SuccessfulTopic(BaseModel):
    topic: str
    score: float
    evidence: str
    learned_at: Optional[datetime] = None


class FailedTopic(BaseModel):
    topic: str
    score: float
    reason: str
    learned_at: Optional[datetime] = None


class CreatorProfileMemory(BaseModel):
    niche: Optional[str] = None
    subscriber_count: Optional[int] = None
    upload_frequency: Optional[str] = None
    content_style: Optional[str] = None


class Preferences(BaseModel):
    categories: List[str] = []
    publish_times: List[str] = []
    topics_to_avoid: List[str] = []


class LearningHistory(BaseModel):
    successful_topics: List[SuccessfulTopic] = []
    failed_topics: List[FailedTopic] = []


class MemoryResponse(BaseModel):
    creator_profile: CreatorProfileMemory
    preferences: Preferences
    learning_history: LearningHistory
    all_memories: Dict[str, List[MemoryEntry]] = {}


class AutoUpdateTrigger(BaseModel):
    source: str  # trend_analysis, recommendation_generation, pipeline_run
    data: dict
