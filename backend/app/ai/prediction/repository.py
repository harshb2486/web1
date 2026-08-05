from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.video import Video
from app.models.feature_vector import FeatureVector
from app.models.profile import CreatorProfile


class PredictionRepository:
    async def get_videos(self, user_id: str, db: AsyncSession) -> List[Video]:
        result = await db.execute(
            select(Video).where(Video.user_id == user_id).order_by(Video.published_at.desc())
        )
        return result.scalars().all()

    async def get_features(self, user_id: str, db: AsyncSession) -> Optional[FeatureVector]:
        result = await db.execute(
            select(FeatureVector).where(FeatureVector.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def get_profile(self, user_id: str, db: AsyncSession) -> Optional[CreatorProfile]:
        result = await db.execute(
            select(CreatorProfile).where(CreatorProfile.user_id == user_id)
        )
        return result.scalar_one_or_none()

    def calc_avg_views(self, videos: List[Video]) -> int:
        if not videos:
            return 150000
        return sum(v.views for v in videos) // len(videos)

    def calc_avg_revenue(self, videos: List[Video]) -> float:
        if not videos:
            return 3.5
        total_revenue = sum(v.revenue for v in videos)
        total_views = sum(v.views for v in videos)
        if total_views == 0:
            return 3.5
        return (total_revenue / total_views) * 1000
