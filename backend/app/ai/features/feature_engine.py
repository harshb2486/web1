from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.video import Video
from app.models.profile import CreatorProfile
from app.models.trend import Trend
from app.models.feature_vector import FeatureVector
from app.ai.features.feature_store import FeatureStore


class FeatureEngine:
    def __init__(self):
        self.store = FeatureStore()

    async def compute_all(self, user_id: str, db: AsyncSession) -> FeatureVector:
        videos = await self._get_videos(user_id, db)
        profile = await self._get_profile(user_id, db)
        trends = await self._get_trends(user_id, db)

        vector = FeatureVector(
            user_id=user_id,
            ctr=self._calc_ctr(videos),
            avg_watch_time=self._calc_avg_watch_time(videos),
            growth_pct=self._calc_growth(profile),
            retention_rate=self._calc_retention(videos),
            upload_frequency=self._calc_upload_frequency(videos),
            view_velocity=self._calc_view_velocity(videos),
            engagement_score=self._calc_engagement(videos),
            trend_score=self._calc_trend_alignment(trends, profile),
            competition_score=self._calc_competition(trends),
            computed_at=datetime.now(timezone.utc),
        )
        return await self.store.save(vector, db)

    async def _get_videos(self, user_id: str, db: AsyncSession):
        result = await db.execute(select(Video).where(Video.user_id == user_id))
        return result.scalars().all()

    async def _get_profile(self, user_id: str, db: AsyncSession):
        result = await db.execute(select(CreatorProfile).where(CreatorProfile.user_id == user_id))
        return result.scalar_one_or_none()

    async def _get_trends(self, user_id: str, db: AsyncSession):
        result = await db.execute(select(Trend).where(Trend.user_id == user_id))
        return result.scalars().all()

    def _calc_ctr(self, videos) -> float:
        if not videos:
            return 0.05
        total_views = sum(v.views for v in videos)
        if total_views == 0:
            return 0.05
        impressions = total_views * 10
        return min(total_views / impressions, 0.25)

    def _calc_avg_watch_time(self, videos) -> float:
        if not videos:
            return 300.0
        total_views = sum(v.views for v in videos)
        if total_views == 0:
            return 300.0
        return min(total_views / len(videos) * 0.002, 1200.0)

    def _calc_growth(self, profile) -> float:
        if profile and profile.subscriber_count > 0:
            base = min(profile.subscriber_count / 10000, 10.0)
            return round(base, 1)
        return 0.0

    def _calc_retention(self, videos) -> float:
        if not videos:
            return 0.45
        total_views = sum(v.views for v in videos)
        if total_views == 0:
            return 0.45
        avg_views = total_views / len(videos)
        if avg_views > 100000:
            return 0.65
        elif avg_views > 50000:
            return 0.55
        elif avg_views > 10000:
            return 0.45
        return 0.35

    def _calc_upload_frequency(self, videos) -> float:
        if not videos:
            return 2.0
        return round(len(videos) / 4.0, 1)

    def _calc_view_velocity(self, videos) -> float:
        if not videos:
            return 5000.0
        total_views = sum(v.views for v in videos)
        return round(total_views / max(len(videos), 1) / 24.0, 1)

    def _calc_engagement(self, videos) -> float:
        if not videos:
            return 5.0
        total_views = sum(v.views for v in videos)
        if total_views == 0:
            return 5.0
        avg_views = total_views / len(videos)
        if avg_views > 100000:
            return 8.5
        elif avg_views > 50000:
            return 7.0
        elif avg_views > 10000:
            return 5.5
        return 4.0

    def _calc_trend_alignment(self, trends, profile) -> float:
        if not trends:
            return 50.0
        if profile and profile.niche:
            niche_lower = profile.niche.lower()
            niche_words = niche_lower.split()
            aligned = sum(
                1 for t in trends
                if any(kw in t.topic.lower() for kw in niche_words)
            )
            return min((aligned / max(len(trends), 1)) * 100, 100.0)
        return 50.0

    def _calc_competition(self, trends) -> float:
        if not trends:
            return 50.0
        high = sum(1 for t in trends if t.competition == "High")
        medium = sum(1 for t in trends if t.competition == "Medium")
        score = ((high * 1.0 + medium * 0.5) / max(len(trends), 1)) * 100
        return min(score, 100.0)
