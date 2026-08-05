import logging
from datetime import datetime, timezone, timedelta
from app.celery_app import celery_app

logger = logging.getLogger(__name__)


@celery_app.task(name="app.workers.cleanup.cleanup_old_data", bind=True)
def cleanup_old_data(self):
    import asyncio
    from app.core.database import async_session
    from sqlalchemy import delete
    from app.models.chat_message import ChatMessage
    from app.models.pipeline_job import PipelineJob

    async def _run():
        async with async_session() as db:
            cutoff = datetime.now(timezone.utc) - timedelta(days=30)
            await db.execute(
                delete(ChatMessage).where(ChatMessage.created_at < cutoff)
            )
            await db.execute(
                delete(PipelineJob).where(
                    PipelineJob.status == "completed",
                    PipelineJob.completed_at < cutoff,
                )
            )
            await db.commit()
            logger.info("Cleanup completed: old data removed")
            return {"cleaned": True}

    return asyncio.run(_run())
