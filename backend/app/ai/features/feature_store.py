from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.feature_vector import FeatureVector


class FeatureStore:
    async def get(self, user_id: str, db: AsyncSession) -> Optional[FeatureVector]:
        result = await db.execute(
            select(FeatureVector).where(FeatureVector.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def save(self, vector: FeatureVector, db: AsyncSession) -> FeatureVector:
        existing = await self.get(vector.user_id, db)
        if existing:
            existing.ctr = vector.ctr
            existing.avg_watch_time = vector.avg_watch_time
            existing.growth_pct = vector.growth_pct
            existing.retention_rate = vector.retention_rate
            existing.upload_frequency = vector.upload_frequency
            existing.view_velocity = vector.view_velocity
            existing.engagement_score = vector.engagement_score
            existing.trend_score = vector.trend_score
            existing.competition_score = vector.competition_score
            existing.computed_at = vector.computed_at
            await db.flush()
            return existing
        db.add(vector)
        await db.flush()
        return vector
