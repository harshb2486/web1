from abc import ABC, abstractmethod
from typing import List


class TrendService(ABC):
    @abstractmethod
    async def get_trends(self, user_id: str) -> List[dict]: ...


class RecommendationService(ABC):
    @abstractmethod
    async def get_recommendations(self, user_id: str) -> List[dict]: ...


class PredictionService(ABC):
    @abstractmethod
    async def predict_performance(self, user_id: str, topic: str) -> dict: ...


class CompetitorService(ABC):
    @abstractmethod
    async def get_competitors(self, user_id: str) -> List[dict]: ...
