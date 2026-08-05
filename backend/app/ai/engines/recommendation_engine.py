from typing import List, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.recommendation import Recommendation
from app.models.profile import CreatorProfile
from app.models.trend import Trend
from app.models.competitor import Competitor
from app.models.feature_vector import FeatureVector
from app.ai.engines.prediction_engine import PredictionEngine


class RecommendationEngine:
    def __init__(self):
        self.prediction = PredictionEngine()

    async def generate(self, user_id: str, db: AsyncSession) -> List[Dict]:
        profile = await self._get_profile(user_id, db)
        trends = await self._get_trends(user_id, db)
        competitors = await self._get_competitors(user_id, db)
        features = await self._get_features(user_id, db)

        opportunities = self._calculate_opportunities(trends, competitors, features, profile)
        ranked = self._rank_topics(opportunities)
        recommendations = await self._generate_recommendations(ranked, user_id, db)

        return recommendations

    def _calculate_opportunities(self, trends, competitors, features, profile) -> List[Dict]:
        results = []
        for trend in trends:
            trend_fit = trend.fit / 100.0 if hasattr(trend, 'fit') else 0.5
            momentum = 0.7
            gap_score = 0.6
            competition_discount = 1.0

            for comp in competitors:
                if comp.overlap > 70:
                    competition_discount *= 0.9

            score = (0.35 * momentum) + (0.35 * trend_fit) + (0.3 * gap_score)
            score *= competition_discount

            results.append({
                "topic": trend.topic,
                "score": min(score, 1.0),
                "trend_fit": trend_fit,
                "competition": trend.competition,
                "category": trend.category,
                "searchVolume": trend.search_volume,
                "direction": trend.direction,
                "growthDays": trend.growth_days,
            })
        return results

    def _rank_topics(self, opportunities: List[Dict]) -> List[Dict]:
        return sorted(opportunities, key=lambda x: x["score"], reverse=True)[:10]

    async def _generate_recommendations(self, ranked: List[Dict], user_id: str, db: AsyncSession) -> List[Dict]:
        recommendations = []
        for item in ranked[:5]:
            views = await self.prediction.predict_views(item["topic"], user_id, db)
            revenue = await self.prediction.predict_revenue(views["low"], views["high"], user_id, db)

            confidence = int(item["score"] * 100)
            potential = "high" if confidence >= 75 else "medium" if confidence >= 50 else "low"

            rec_data = {
                "topic": item["topic"],
                "confidence": confidence,
                "evidence": [
                    f"Search volume {item['searchVolume']} with {item['growthDays']} days of growth",
                    f"Competition level: {item['competition']}",
                    f"Your niche alignment: {int(item['trend_fit'] * 100)}%",
                ],
                "expectedViews": views,
                "expectedRevenue": revenue,
                "risks": [f"Competition may increase as topic gains traction"],
                "similarContent": {"title": f"{item['topic']} Explained", "views": views["high"]},
                "publishTime": "Tuesday 7:30 PM EST",
                "category": item["category"],
                "potential": potential,
            }
            recommendations.append(rec_data)

            existing = await db.execute(
                select(Recommendation).where(Recommendation.user_id == user_id, Recommendation.topic == item["topic"])
            )
            existing_rec = existing.scalar_one_or_none()
            if existing_rec:
                existing_rec.confidence = confidence
                existing_rec.evidence = rec_data["evidence"]
                existing_rec.expected_views_low = views["low"]
                existing_rec.expected_views_high = views["high"]
                existing_rec.expected_revenue_low = revenue["low"]
                existing_rec.expected_revenue_high = revenue["high"]
                existing_rec.potential = potential
            else:
                rec = Recommendation(
                    user_id=user_id,
                    topic=item["topic"],
                    confidence=confidence,
                    evidence=rec_data["evidence"],
                    expected_views_low=views["low"],
                    expected_views_high=views["high"],
                    expected_revenue_low=revenue["low"],
                    expected_revenue_high=revenue["high"],
                    risks=rec_data["risks"],
                    similar_content_title=rec_data["similarContent"]["title"],
                    similar_content_views=rec_data["similarContent"]["views"],
                    publish_time=rec_data["publishTime"],
                    category=item["category"],
                    potential=potential,
                )
                db.add(rec)
        await db.flush()
        return recommendations

    async def _get_profile(self, user_id, db):
        r = await db.execute(select(CreatorProfile).where(CreatorProfile.user_id == user_id))
        return r.scalar_one_or_none()

    async def _get_trends(self, user_id, db):
        r = await db.execute(select(Trend).where(Trend.user_id == user_id))
        return r.scalars().all()

    async def _get_competitors(self, user_id, db):
        r = await db.execute(select(Competitor).where(Competitor.user_id == user_id))
        return r.scalars().all()

    async def _get_features(self, user_id, db):
        r = await db.execute(select(FeatureVector).where(FeatureVector.user_id == user_id))
        return r.scalar_one_or_none()
