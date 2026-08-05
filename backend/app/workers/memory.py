import logging
from app.celery_app import celery_app

logger = logging.getLogger(__name__)


@celery_app.task(name="app.workers.memory.update_memory", bind=True)
def update_memory(self, user_id: str, job_id: str = None):
    import asyncio
    from app.core.database import async_session
    from app.ai.memory.service import MemoryService

    async def _run():
        service = MemoryService()
        async with async_session() as db:
            await service.update_from_videos(user_id, db)
            await db.commit()
            logger.info(f"Memory updated for user {user_id}")
            return {"updated": True}

    return asyncio.run(_run())
