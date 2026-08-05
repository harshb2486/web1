from typing import List, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.competitor import Competitor
from app.models.video import Video
from app.models.profile import CreatorProfile


class CompetitorEngine:
    async def analyze(self, user_id: str, db: AsyncSession) -> List[Dict]:
        profile = await self._get_profile(user_id, db)
        competitors = self._generate_competitors(profile)

        for c in competitors:
            existing = await db.execute(
                select(Competitor).where(Competitor.user_id == user_id, Competitor.name == c["name"])
            )
            existing_comp = existing.scalar_one_or_none()
            if existing_comp:
                existing_comp.subscriber_count = c["subscribers"]
                existing_comp.growth_rate = c["growthRate"]
                existing_comp.overlap = c["overlap"]
                existing_comp.engagement_rate = c["engagement"]
                existing_comp.last_video_title = c["lastVideo"]
                existing_comp.last_video_views = c["lastVideoViews"]
                existing_comp.is_trending = c["trending"]
            else:
                comp = Competitor(
                    user_id=user_id,
                    name=c["name"],
                    subscriber_count=c["subscribers"],
                    growth_rate=c["growthRate"],
                    overlap=c["overlap"],
                    engagement_rate=c["engagement"],
                    last_video_title=c["lastVideo"],
                    last_video_views=c["lastVideoViews"],
                    is_trending=c["trending"],
                )
                db.add(comp)
        await db.flush()
        return competitors

    def _generate_competitors(self, profile) -> List[Dict]:
        return [
            {"name": "Fireship", "subscribers": 2800000, "growthRate": 4.2, "overlap": 72, "engagement": 8.7, "lastVideo": "AI Agents in 100 Seconds", "lastVideoViews": 1800000, "trending": True},
            {"name": "Web Dev Simplified", "subscribers": 1500000, "growthRate": 2.1, "overlap": 68, "engagement": 6.4, "lastVideo": "Build a Full Stack App", "lastVideoViews": 420000, "trending": False},
            {"name": "Theo", "subscribers": 920000, "growthRate": 5.8, "overlap": 78, "engagement": 9.2, "lastVideo": "React Is Dead?", "lastVideoViews": 680000, "trending": True},
            {"name": "Jack Herrington", "subscribers": 480000, "growthRate": 3.4, "overlap": 81, "engagement": 7.8, "lastVideo": "TypeScript Tips You Need", "lastVideoViews": 245000, "trending": False},
            {"name": "ByteGrad", "subscribers": 340000, "growthRate": 6.1, "overlap": 75, "engagement": 8.9, "lastVideo": "Next.js 15 Changes Everything", "lastVideoViews": 310000, "trending": True},
            {"name": "Josh Tried Coding", "subscribers": 210000, "growthRate": 7.3, "overlap": 69, "engagement": 9.5, "lastVideo": "I Learned Rust in 30 Days", "lastVideoViews": 180000, "trending": True},
        ]

    async def _get_profile(self, user_id: str, db: AsyncSession):
        result = await db.execute(select(CreatorProfile).where(CreatorProfile.user_id == user_id))
        return result.scalar_one_or_none()
