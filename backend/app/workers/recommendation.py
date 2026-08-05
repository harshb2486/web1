import logging
from app.celery_app import celery_app

logger = logging.getLogger(__name__)


@celery_app.task(name="app.workers.recommendation.generate_recommendations", bind=True)
def generate_recommendations(self, user_id: str, job_id: str = None):
    import asyncio
    from app.core.database import async_session
    from app.ai.engines.recommendation_engine import RecommendationEngine

    async def _run():
        engine = RecommendationEngine()
        async with async_session() as db:
            result = await engine.generate(user_id, db)
            await db.commit()
            logger.info(f"Recommendations generated for user {user_id}: {len(result)} recommendations")
            return {"recommendations": len(result)}

    return asyncio.run(_run())
