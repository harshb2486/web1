from typing import List, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.trend import Trend
from app.models.profile import CreatorProfile
from app.models.feature_vector import FeatureVector


class TrendEngine:
    async def analyze(self, user_id: str, db: AsyncSession) -> List[Dict]:
        profile = await self._get_profile(user_id, db)
        features = await self._get_features(user_id, db)
        niche = profile.niche if profile else "Technology"

        trends = self._generate_trend_candidates(niche, features)
        ranked = self._rank_trends(trends, niche)
        scored = self._score_trends(ranked, features)

        for t in scored:
            existing = await db.execute(
                select(Trend).where(Trend.user_id == user_id, Trend.topic == t["topic"])
            )
            existing_trend = existing.scalar_one_or_none()
            if existing_trend:
                existing_trend.growth_days = t["growthDays"]
                existing_trend.competition = t["competition"]
                existing_trend.fit = t["fit"]
                existing_trend.search_volume = t["searchVolume"]
                existing_trend.direction = t["direction"]
            else:
                trend = Trend(
                    user_id=user_id,
                    topic=t["topic"],
                    growth_days=t["growthDays"],
                    competition=t["competition"],
                    fit=t["fit"],
                    search_volume=t["searchVolume"],
                    category=t["category"],
                    country=t.get("country", "Global"),
                    direction=t["direction"],
                )
                db.add(trend)
        await db.flush()
        return scored

    def _generate_trend_candidates(self, niche: str, features) -> List[Dict]:
        return [
            {"topic": "AI Agents", "growthDays": 18, "competition": "Medium", "searchVolume": "+340%", "category": "Tech", "country": "Global", "direction": "up", "raw_momentum": 0.85},
            {"topic": "MCP Protocol", "growthDays": 12, "competition": "Low", "searchVolume": "+520%", "category": "Tech", "country": "United States", "direction": "up", "raw_momentum": 0.92},
            {"topic": "Rust for Web Dev", "growthDays": 24, "competition": "Low", "searchVolume": "+180%", "category": "Tech", "country": "Global", "direction": "up", "raw_momentum": 0.65},
            {"topic": "AI Video Generation", "growthDays": 15, "competition": "High", "searchVolume": "+290%", "category": "Creative", "country": "India", "direction": "up", "raw_momentum": 0.78},
            {"topic": "No-Code SaaS", "growthDays": 21, "competition": "Medium", "searchVolume": "+160%", "category": "Business", "country": "United States", "direction": "stable", "raw_momentum": 0.55},
            {"topic": "Local LLM Setup", "growthDays": 9, "competition": "Low", "searchVolume": "+410%", "category": "Tech", "country": "Germany", "direction": "up", "raw_momentum": 0.88},
            {"topic": "GPT-5 Features", "growthDays": 6, "competition": "High", "searchVolume": "+680%", "category": "AI", "country": "Global", "direction": "up", "raw_momentum": 0.95},
            {"topic": "TypeScript 6.0", "growthDays": 3, "competition": "Low", "searchVolume": "+220%", "category": "Tech", "country": "Global", "direction": "up", "raw_momentum": 0.72},
            {"topic": "AI Coding Agents", "growthDays": 14, "competition": "Medium", "searchVolume": "+390%", "category": "Tech", "country": "United States", "direction": "up", "raw_momentum": 0.82},
            {"topic": "React Server Components", "growthDays": 16, "competition": "Medium", "searchVolume": "+210%", "category": "Tech", "country": "Global", "direction": "up", "raw_momentum": 0.68},
        ]

    def _rank_trends(self, trends: List[Dict], niche: str) -> List[Dict]:
        niche_lower = niche.lower()
        for t in trends:
            topic_lower = t["topic"].lower()
            niche_words = niche_lower.split()
            match = sum(1 for w in niche_words if w in topic_lower)
            t["niche_match"] = match / max(len(niche_words), 1)
        return sorted(trends, key=lambda x: x.get("niche_match", 0), reverse=True)

    def _score_trends(self, trends: List[Dict], features) -> List[Dict]:
        comp_map = {"Low": 0.2, "Medium": 0.5, "High": 0.8}
        for t in trends:
            momentum = t.get("raw_momentum", 0.5)
            niche = t.get("niche_match", 0.5)
            competition = comp_map.get(t["competition"], 0.5)
            score = (0.4 * momentum) + (0.4 * niche) + (0.2 * (1 - competition))
            t["fit"] = min(int(score * 100), 100)
        return trends
