import logging
from app.celery_app import celery_app

logger = logging.getLogger(__name__)


@celery_app.task(name="app.workers.trend.sync_trends", bind=True)
def sync_trends(self, user_id: str, job_id: str = None):
    import asyncio
    from app.core.database import async_session
    from app.ai.engines.trend_engine import TrendEngine

    async def _run():
        engine = TrendEngine()
        async with async_session() as db:
            result = await engine.analyze(user_id, db)
            await db.commit()
            logger.info(f"Trends synced for user {user_id}: {len(result)} trends")
            return {"trends": len(result)}

    return asyncio.run(_run())
