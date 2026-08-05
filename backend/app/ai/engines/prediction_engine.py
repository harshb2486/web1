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
        trend_multiplier = 1.2
        competition_discount = 0.85

        estimated = base_views * trend_multiplier * competition_discount
        return {
            "low": int(estimated * 0.6),
            "high": int(estimated * 1.4),
        }

    async def predict_revenue(self, views_low: int, views_high: int, user_id: str, db: AsyncSession) -> Dict:
        rpm_low = 2.0
        rpm_high = 5.0
        return {
            "low": int(views_low / 1000 * rpm_low),
            "high": int(views_high / 1000 * rpm_high),
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
            return 150000
        total = sum(v.views for v in videos)
        return total // max(len(videos), 1)

    async def _get_features(self, user_id: str, db: AsyncSession):
        result = await db.execute(select(FeatureVector).where(FeatureVector.user_id == user_id))
        return result.scalar_one_or_none()

    async def _get_videos(self, user_id: str, db: AsyncSession):
        result = await db.execute(select(Video).where(Video.user_id == user_id))
        return result.scalars().all()
