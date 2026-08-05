import uuid
from datetime import datetime, timezone
from typing import Dict, Optional

from app.celery_app import celery_app


class JobOrchestrator:
    async def run_pipeline(self, user_id: str) -> str:
        job_id = str(uuid.uuid4())
        celery_app.send_task(
            "app.workers.trend.sync_trends",
            args=[user_id, job_id],
            queue="ai",
        )
        celery_app.send_task(
            "app.workers.recommendation.generate_recommendations",
            args=[user_id, job_id],
            queue="ai",
        )
        celery_app.send_task(
            "app.workers.prediction.generate_predictions",
            args=[user_id, job_id],
            queue="ai",
        )
        celery_app.send_task(
            "app.workers.memory.update_memory",
            args=[user_id, job_id],
            queue="ai",
        )
        celery_app.send_task(
            "app.workers.notification.check_notifications",
            args=[user_id],
            queue="ai",
        )
        return job_id

    async def sync_trends(self, user_id: str) -> str:
        job_id = str(uuid.uuid4())
        celery_app.send_task(
            "app.workers.trend.sync_trends",
            args=[user_id, job_id],
            queue="ai",
        )
        return job_id

    async def sync_competitors(self, user_id: str) -> str:
        job_id = str(uuid.uuid4())
        celery_app.send_task(
            "app.workers.competitor.sync_competitors",
            args=[user_id, job_id],
            queue="ai",
        )
        return job_id

    async def generate_recommendations(self, user_id: str) -> str:
        job_id = str(uuid.uuid4())
        celery_app.send_task(
            "app.workers.recommendation.generate_recommendations",
            args=[user_id, job_id],
            queue="ai",
        )
        return job_id

    async def generate_predictions(self, user_id: str) -> str:
        job_id = str(uuid.uuid4())
        celery_app.send_task(
            "app.workers.prediction.generate_predictions",
            args=[user_id, job_id],
            queue="ai",
        )
        return job_id

    async def update_memory(self, user_id: str) -> str:
        job_id = str(uuid.uuid4())
        celery_app.send_task(
            "app.workers.memory.update_memory",
            args=[user_id, job_id],
            queue="ai",
        )
        return job_id

    async def analyze_video(self, user_id: str, video_id: str) -> str:
        job_id = str(uuid.uuid4())
        celery_app.send_task(
            "app.workers.analytics.analyze_video",
            args=[user_id, video_id, job_id],
            queue="ai",
        )
        return job_id

    async def get_status(self, job_id: str) -> Dict:
        result = celery_app.AsyncResult(job_id)
        return {
            "id": job_id,
            "status": result.status,
            "result": result.result if result.ready() else None,
        }
