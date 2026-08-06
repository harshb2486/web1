from typing import List, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.competitor import Competitor
from app.models.profile import CreatorProfile


COMPETITOR_POOLS = {
    "technology": [
        {"name": "Fireship", "base_subs": 2800000, "growth": 4.2, "overlap": 72, "engagement": 8.7},
        {"name": "Web Dev Simplified", "base_subs": 1500000, "growth": 2.1, "overlap": 68, "engagement": 6.4},
        {"name": "Theo", "base_subs": 920000, "growth": 5.8, "overlap": 78, "engagement": 9.2},
        {"name": "Jack Herrington", "base_subs": 480000, "growth": 3.4, "overlap": 81, "engagement": 7.8},
        {"name": "ByteGrad", "base_subs": 340000, "growth": 6.1, "overlap": 75, "engagement": 8.9},
        {"name": "Josh Tried Coding", "base_subs": 210000, "growth": 7.3, "overlap": 69, "engagement": 9.5},
    ],
    "business": [
        {"name": "Ali Abdaal", "base_subs": 4200000, "growth": 3.8, "overlap": 65, "engagement": 7.2},
        {"name": "Pat Flynn", "base_subs": 1100000, "growth": 1.9, "overlap": 58, "engagement": 6.8},
        {"name": "Thomas Frank", "base_subs": 2900000, "growth": 4.5, "overlap": 72, "engagement": 8.1},
        {"name": "Mike Winnet", "base_subs": 450000, "growth": 8.2, "overlap": 45, "engagement": 7.5},
        {"name": "Ryan Daniel Moran", "base_subs": 380000, "growth": 5.6, "overlap": 52, "engagement": 6.9},
    ],
    "lifestyle": [
        {"name": "Matt D'Avella", "base_subs": 3800000, "growth": 2.8, "overlap": 60, "engagement": 8.5},
        {"name": "Nathaniel Drew", "base_subs": 1200000, "growth": 4.1, "overlap": 55, "engagement": 7.8},
        {"name": "Matt D'Avella", "base_subs": 3800000, "growth": 2.8, "overlap": 60, "engagement": 8.5},
        {"name": "Pick Up Limes", "base_subs": 2100000, "growth": 3.2, "overlap": 48, "engagement": 9.1},
    ],
    "default": [
        {"name": "CreatorTech Hub", "base_subs": 285000, "growth": 12.5, "overlap": 78, "engagement": 4.2},
        {"name": "Digital Nomad Academy", "base_subs": 156000, "growth": 8.3, "overlap": 45, "engagement": 3.8},
        {"name": "Content Strategy Lab", "base_subs": 420000, "growth": 15.2, "overlap": 62, "engagement": 5.1},
        {"name": "YouTube Growth Secrets", "base_subs": 89000, "growth": 22.1, "overlap": 35, "engagement": 6.2},
    ],
}

TOPIC_POOLS = {
    "technology": [
        ("AI Agents in 100 Seconds", 1800000),
        ("Build a Full Stack App", 420000),
        ("React Is Dead?", 680000),
        ("TypeScript Tips You Need", 245000),
        ("Next.js 15 Changes Everything", 310000),
        ("I Learned Rust in 30 Days", 180000),
    ],
    "business": [
        ("How I Make $10K/Month Passive Income", 850000),
        ("Start a Business in 24 Hours", 620000),
        ("Financial Freedom Blueprint", 430000),
        ("Amazon FBA Complete Guide", 290000),
        ("Dropshipping in 2025", 380000),
    ],
    "lifestyle": [
        ("Minimalist Morning Routine", 720000),
        ("How I Structure My Day", 540000),
        ("Digital Detox Challenge", 380000),
        ("Productivity System That Works", 610000),
    ],
    "default": [
        ("AI Changed How I Create", 125000),
        ("Passive Income for Creators", 89000),
        ("Viral Content Formula", 340000),
        ("How I Got 1M Subs", 560000),
    ],
}


class CompetitorEngine:
    async def analyze(self, user_id: str, db: AsyncSession) -> List[Dict]:
        profile = await self._get_profile(user_id, db)
        niche = self._get_niche(profile)
        competitors = self._generate_competitors(niche, profile)

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

    def _get_niche(self, profile) -> str:
        if not profile or not profile.niche:
            return "default"
        niche_lower = profile.niche.lower()
        for key in COMPETITOR_POOLS:
            if key in niche_lower:
                return key
        return "default"

    def _generate_competitors(self, niche: str, profile) -> List[Dict]:
        pool = COMPETITOR_POOLS.get(niche, COMPETITOR_POOLS["default"])
        topic_pool = TOPIC_POOLS.get(niche, TOPIC_POOLS["default"])

        user_subs = profile.subscriber_count if profile and profile.subscriber_count else 100000

        competitors = []
        for i, c in enumerate(pool[:6]):
            sub_ratio = user_subs / max(c["base_subs"], 1)
            overlap = max(30, min(90, int(c["overlap"] * (1 - abs(sub_ratio - 1) * 0.3))))
            trending = c["growth"] > 5.0 or (i % 2 == 0)

            topic_title, topic_views = topic_pool[i % len(topic_pool)]

            competitors.append({
                "name": c["name"],
                "subscribers": c["base_subs"],
                "growthRate": c["growth"],
                "overlap": overlap,
                "engagement": c["engagement"],
                "lastVideo": topic_title,
                "lastVideoViews": topic_views,
                "trending": trending,
            })

        return competitors

    async def _get_profile(self, user_id: str, db: AsyncSession):
        result = await db.execute(select(CreatorProfile).where(CreatorProfile.user_id == user_id))
        return result.scalar_one_or_none()
