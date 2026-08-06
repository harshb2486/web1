from typing import Dict, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.video import Video
from app.models.feature_vector import FeatureVector


class PredictionEngine:
    async def predict_views(self, topic: str, user_id: str, db: AsyncSession) -> Dict:
        features = await self._get_features(user_id, db)
        videos = await self._get_videos(user_id, db)

        base_views = self._calc_base_views(videos)
        trend_multiplier = 1.0 + (0.3 if features and features.trend_score > 60 else 0.1)
        competition_discount = 0.9 if features and features.competition_score > 70 else 1.0

        estimated = base_views * trend_multiplier * competition_discount
        return {
            "low": int(estimated * 0.6),
            "high": int(estimated * 1.4),
        }

    async def predict_revenue(self, views_low: int, views_high: int, user_id: str, db: AsyncSession) -> Dict:
        videos = await self._get_videos(user_id, db)
        rpm = self._calc_rpm(videos)
        return {
            "low": int(views_low / 1000 * rpm * 0.7),
            "high": int(views_high / 1000 * rpm * 1.3),
        }

    async def predict_trajectory(self, trend: Dict, user_id: str, db: AsyncSession) -> Dict:
        momentum = trend.get("raw_momentum", 0.5)
        return {
            "day_7": min(momentum * 100, 100),
            "day_14": min(momentum * 90, 100),
            "day_30": min(momentum * 70, 100),
        }

    def _calc_base_views(self, videos) -> int:
        if not videos:
            return 50000
        views = [v.views for v in videos if v.views > 0]
        if not views:
            return 50000
        return sum(views) // len(views)

    def _calc_rpm(self, videos) -> float:
        if not videos:
            return 3.5
        total_revenue = sum(v.revenue for v in videos)
        total_views = sum(v.views for v in videos)
        if total_views == 0:
            return 3.5
        rpm = (total_revenue / total_views) * 1000
        return max(1.0, min(rpm, 15.0))

    async def _get_features(self, user_id: str, db: AsyncSession):
        result = await db.execute(select(FeatureVector).where(FeatureVector.user_id == user_id))
        return result.scalar_one_or_none()

    async def _get_videos(self, user_id: str, db: AsyncSession):
        result = await db.execute(select(Video).where(Video.user_id == user_id))
        return result.scalars().all()
