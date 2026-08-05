import logging
from datetime import datetime, timezone, timedelta
from app.celery_app import celery_app

logger = logging.getLogger(__name__)


@celery_app.task(name="app.workers.analytics.analyze_video", bind=True)
def analyze_video(self, user_id: str, video_id: str, job_id: str = None):
    import asyncio
    from app.core.database import async_session
    from app.ai.prediction.service import PredictionService

    async def _run():
        service = PredictionService()
        async with async_session() as db:
            trend_data = {"raw_momentum": 0.6, "competition": "Medium", "fit": 65}
            pred = await service.predict_video("analysis", trend_data, user_id, db)
            logger.info(f"Video {video_id} analyzed for user {user_id}")
            return {"video_id": video_id, "views": pred.views.prediction}

    return asyncio.run(_run())
