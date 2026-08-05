import logging
from app.celery_app import celery_app

logger = logging.getLogger(__name__)


@celery_app.task(name="app.workers.competitor.sync_competitors", bind=True)
def sync_competitors(self, user_id: str, job_id: str = None):
    import asyncio
    from app.core.database import async_session
    from app.ai.engines.competitor_engine import CompetitorEngine

    async def _run():
        engine = CompetitorEngine()
        async with async_session() as db:
            result = await engine.analyze(user_id, db)
            await db.commit()
            logger.info(f"Competitors synced for user {user_id}: {len(result)} competitors")
            return {"competitors": len(result)}

    return asyncio.run(_run())
