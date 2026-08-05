import logging
from app.celery_app import celery_app

logger = logging.getLogger(__name__)


@celery_app.task(name="app.workers.prediction.generate_predictions", bind=True)
def generate_predictions(self, user_id: str, job_id: str = None):
    import asyncio
    from app.core.database import async_session
    from app.ai.prediction.service import PredictionService

    async def _run():
        service = PredictionService()
        async with async_session() as db:
            topics = ["AI Agents", "MCP Protocol", "Rust for Web Dev"]
            results = []
            for topic in topics:
                trend_data = {"raw_momentum": 0.7, "competition": "Medium", "fit": 70}
                pred = await service.predict_video(topic, trend_data, user_id, db)
                results.append({"topic": topic, "views": pred.views.prediction})
            logger.info(f"Predictions generated for user {user_id}: {len(results)} predictions")
            return {"predictions": len(results)}

    return asyncio.run(_run())
