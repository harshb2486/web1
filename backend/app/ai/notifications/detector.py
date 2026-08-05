from typing import List, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.notification import Notification
from app.models.trend import Trend
from app.models.competitor import Competitor
from app.models.recommendation import Recommendation


NOTIFICATION_RULES = [
    {"name": "trend_spike", "check": "trend_fit > 85", "type": "info", "template": "{topic} trending with {volume} search volume"},
    {"name": "competitor_alert", "check": "competitor_trending", "type": "info", "template": "{name} published a new video with {views} views"},
    {"name": "revenue_milestone", "check": "revenue_growth > 10", "type": "success", "template": "You've earned ${amount} this month"},
    {"name": "recommendation_ready", "check": "new_recommendations", "type": "info", "template": "We have {count} new content ideas for you"},
]


class NotificationDetector:
    async def detect(self, user_id: str, db: AsyncSession) -> List[Dict]:
        triggered = []

        trends = await self._get_trends(user_id, db)
        for t in trends:
            if t.fit > 85:
                triggered.append({
                    "title": "Trend detected",
                    "message": f"{t.topic} trending with {t.search_volume} search volume",
                    "type": "info",
                })

        competitors = await self._get_competitors(user_id, db)
        for c in competitors:
            if c.is_trending:
                triggered.append({
                    "title": "Competitor alert",
                    "message": f"{c.name} published a new video with {c.last_video_views // 1000}K views",
                    "type": "info",
                })

        recs = await self._get_recommendations(user_id, db)
        if len(recs) > 0:
            triggered.append({
                "title": "New recommendations",
                "message": f"We have {len(recs)} new content ideas for you",
                "type": "success",
            })

        return triggered

    async def _get_trends(self, user_id, db):
        r = await db.execute(select(Trend).where(Trend.user_id == user_id))
        return r.scalars().all()

    async def _get_competitors(self, user_id, db):
        r = await db.execute(select(Competitor).where(Competitor.user_id == user_id))
        return r.scalars().all()

    async def _get_recommendations(self, user_id, db):
        r = await db.execute(select(Recommendation).where(Recommendation.user_id == user_id))
        return r.scalars().all()


class NotificationEmitter:
    async def emit(self, user_id: str, notifications: List[Dict], db: AsyncSession) -> List[Notification]:
        emitted = []
        for n in notifications:
            existing = await db.execute(
                select(Notification).where(
                    Notification.user_id == user_id,
                    Notification.title == n["title"],
                    Notification.is_read == False,
                )
            )
            if existing.first():
                continue

            notif = Notification(
                user_id=user_id,
                title=n["title"],
                message=n["message"],
                type=n.get("type", "info"),
                is_read=False,
            )
            db.add(notif)
            emitted.append(notif)
        await db.flush()
        return emitted
