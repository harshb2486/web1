from typing import List, Dict
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.notifications.repository import NotificationRepository
from app.ai.notifications.schemas import NotificationResponse


class NotificationService:
    def __init__(self):
        self.repo = NotificationRepository()

    async def detect_and_notify(self, user_id: str, db: AsyncSession) -> List[NotificationResponse]:
        triggered = []

        trends = await self.repo.get_trends(user_id, db)
        for t in trends:
            if t.fit > 85:
                title = f"Trend Alert: {t.topic}"
                if not await self.repo.exists_recent(user_id, title, db):
                    await self.repo.create(
                        user_id, "trend_alert", "high", title,
                        f"{t.topic} trending with {t.search_volume} search volume and {t.fit}% fit",
                        db,
                    )
                    triggered.append(NotificationResponse(
                        id="", type="trend_alert", priority="high",
                        title=title,
                        message=f"{t.topic} trending with {t.search_volume} search volume",
                        read=False,
                    ))

        competitors = await self.repo.get_competitors(user_id, db)
        for c in competitors:
            if c.is_trending:
                title = f"Competitor Alert: {c.name}"
                if not await self.repo.exists_recent(user_id, title, db):
                    await self.repo.create(
                        user_id, "competitor_alert", "medium", title,
                        f"{c.name} published a new video with {c.last_video_views:,} views",
                        db,
                    )
                    triggered.append(NotificationResponse(
                        id="", type="competitor_alert", priority="medium",
                        title=title,
                        message=f"{c.name} published with {c.last_video_views:,} views",
                        read=False,
                    ))

        recs = await self.repo.get_recommendations(user_id, db)
        if len(recs) > 0:
            title = "New Recommendations"
            if not await self.repo.exists_recent(user_id, title, db):
                await self.repo.create(
                    user_id, "recommendation", "low", title,
                    f"We have {len(recs)} new content ideas for you",
                    db,
                )
                triggered.append(NotificationResponse(
                    id="", type="recommendation", priority="low",
                    title=title,
                    message=f"{len(recs)} new content ideas available",
                    read=False,
                ))

        return triggered

    async def get_all(self, user_id: str, db: AsyncSession) -> List[NotificationResponse]:
        notifs = await self.repo.get_all(user_id, db)
        return [
            NotificationResponse(
                id=n.id, type=n.type, priority="medium",
                title=n.title, message=n.message, read=n.is_read,
            )
            for n in notifs
        ]

    async def get_unread(self, user_id: str, db: AsyncSession) -> List[NotificationResponse]:
        notifs = await self.repo.get_unread(user_id, db)
        return [
            NotificationResponse(
                id=n.id, type=n.type, priority="medium",
                title=n.title, message=n.message, read=n.is_read,
            )
            for n in notifs
        ]

    async def mark_read(self, user_id: str, notification_id: str, db: AsyncSession) -> bool:
        return await self.repo.mark_read(user_id, notification_id, db)

    async def mark_all_read(self, user_id: str, db: AsyncSession) -> int:
        return await self.repo.mark_all_read(user_id, db)
