from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.notification import Notification
from app.models.trend import Trend
from app.models.competitor import Competitor
from app.models.recommendation import Recommendation


class NotificationRepository:
    async def get_all(self, user_id: str, db: AsyncSession) -> List[Notification]:
        result = await db.execute(
            select(Notification).where(Notification.user_id == user_id)
        )
        return result.scalars().all()

    async def get_unread(self, user_id: str, db: AsyncSession) -> List[Notification]:
        result = await db.execute(
            select(Notification).where(
                Notification.user_id == user_id,
                Notification.is_read == False,
            )
        )
        return result.scalars().all()

    async def create(self, user_id: str, notification_type: str, priority: str, title: str, message: str, db: AsyncSession) -> Notification:
        notif = Notification(
            user_id=user_id,
            type=notification_type,
            title=title,
            message=message,
            is_read=False,
        )
        db.add(notif)
        await db.flush()
        return notif

    async def mark_read(self, user_id: str, notification_id: str, db: AsyncSession) -> bool:
        result = await db.execute(
            select(Notification).where(
                Notification.id == notification_id,
                Notification.user_id == user_id,
            )
        )
        notif = result.scalar_one_or_none()
        if notif:
            notif.is_read = True
            await db.flush()
            return True
        return False

    async def mark_all_read(self, user_id: str, db: AsyncSession) -> int:
        result = await db.execute(
            select(Notification).where(
                Notification.user_id == user_id,
                Notification.is_read == False,
            )
        )
        notifs = result.scalars().all()
        for n in notifs:
            n.is_read = True
        await db.flush()
        return len(notifs)

    async def get_trends(self, user_id: str, db: AsyncSession) -> List[Trend]:
        result = await db.execute(
            select(Trend).where(Trend.user_id == user_id)
        )
        return result.scalars().all()

    async def get_competitors(self, user_id: str, db: AsyncSession) -> List[Competitor]:
        result = await db.execute(
            select(Competitor).where(Competitor.user_id == user_id)
        )
        return result.scalars().all()

    async def get_recommendations(self, user_id: str, db: AsyncSession) -> List[Recommendation]:
        result = await db.execute(
            select(Recommendation).where(Recommendation.user_id == user_id)
        )
        return result.scalars().all()

    async def exists_recent(self, user_id: str, title: str, db: AsyncSession) -> bool:
        result = await db.execute(
            select(Notification).where(
                Notification.user_id == user_id,
                Notification.title == title,
            ).limit(1)
        )
        return result.scalar_one_or_none() is not None
