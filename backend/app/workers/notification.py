import logging
from app.celery_app import celery_app

logger = logging.getLogger(__name__)


@celery_app.task(name="app.workers.notification.check_notifications", bind=True)
def check_notifications(self, user_id: str = None):
    import asyncio
    from app.core.database import async_session
    from app.ai.notifications.service import NotificationService

    async def _run():
        service = NotificationService()
        async with async_session() as db:
            if user_id:
                triggered = await service.detect_and_notify(user_id, db)
                await db.commit()
                logger.info(f"Notifications checked for user {user_id}: {len(triggered)} triggered")
                return {"triggered": len(triggered)}
            else:
                logger.info("Notification check completed (all users)")
                return {"triggered": 0}

    return asyncio.run(_run())
