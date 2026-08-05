from typing import List, Dict
from app.ai.processors.base import BaseProcessor


class EngagementProcessor(BaseProcessor):
    async def process(self, signals: List[Dict]) -> List[Dict]:
        for signal in signals:
            metrics = signal.get("metrics", {})
            signal["engagement_score"] = self._calc_engagement(metrics)
        return signals

    def _calc_engagement(self, metrics: Dict) -> float:
        views = metrics.get("views", 0)
        likes = metrics.get("likes", 0)
        comments = metrics.get("comments", 0)
        score = metrics.get("score", 0)

        if views > 0:
            engagement = (likes + comments * 2) / views
            return min(engagement * 100, 100.0)
        elif score > 0:
            return min(score / 100, 100.0)
        return 0.0
