import uuid
import logging
from datetime import datetime, timezone
from typing import Dict, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.pipeline_job import PipelineJob

logger = logging.getLogger(__name__)


class JobOrchestrator:
    async def run_pipeline(self, user_id: str, db: AsyncSession) -> str:
        job = PipelineJob(
            user_id=user_id,
            job_type="full_pipeline",
            status="queued",
            progress=0,
        )
        db.add(job)
        await db.flush()

        try:
            from app.celery_app import celery_app
            if celery_app:
                celery_app.send_task("app.workers.trend.sync_trends", args=[user_id, job.id], queue="ai")
                celery_app.send_task("app.workers.recommendation.generate_recommendations", args=[user_id, job.id], queue="ai")
                celery_app.send_task("app.workers.prediction.generate_predictions", args=[user_id, job.id], queue="ai")
                celery_app.send_task("app.workers.memory.update_memory", args=[user_id, job.id], queue="ai")
                celery_app.send_task("app.workers.notification.check_notifications", args=[user_id], queue="ai")
            else:
                job.status = "completed"
                job.result = {"note": "Celery not available, tasks queued for manual execution"}
                await db.flush()
        except Exception as e:
            logger.warning(f"Celery not available: {e}")
            job.status = "completed"
            job.result = {"note": "Running in demo mode without background workers"}
            await db.flush()

        return job.id

    async def sync_trends(self, user_id: str, db: AsyncSession) -> str:
        job = PipelineJob(user_id=user_id, job_type="sync_trends", status="queued")
        db.add(job)
        await db.flush()
        self._send_task("app.workers.trend.sync_trends", [user_id, job.id])
        return job.id

    async def sync_competitors(self, user_id: str, db: AsyncSession) -> str:
        job = PipelineJob(user_id=user_id, job_type="sync_competitors", status="queued")
        db.add(job)
        await db.flush()
        self._send_task("app.workers.competitor.sync_competitors", [user_id, job.id])
        return job.id

    async def generate_recommendations(self, user_id: str, db: AsyncSession) -> str:
        job = PipelineJob(user_id=user_id, job_type="generate_recommendations", status="queued")
        db.add(job)
        await db.flush()
        self._send_task("app.workers.recommendation.generate_recommendations", [user_id, job.id])
        return job.id

    async def generate_predictions(self, user_id: str, db: AsyncSession) -> str:
        job = PipelineJob(user_id=user_id, job_type="generate_predictions", status="queued")
        db.add(job)
        await db.flush()
        self._send_task("app.workers.prediction.generate_predictions", [user_id, job.id])
        return job.id

    async def update_memory(self, user_id: str, db: AsyncSession) -> str:
        job = PipelineJob(user_id=user_id, job_type="update_memory", status="queued")
        db.add(job)
        await db.flush()
        self._send_task("app.workers.memory.update_memory", [user_id, job.id])
        return job.id

    def _send_task(self, task_name: str, args: list):
        try:
            from app.celery_app import celery_app
            if celery_app:
                celery_app.send_task(task_name, args=args, queue="ai")
        except Exception as e:
            logger.warning(f"Celery task not sent: {e}")

    async def get_status(self, job_id: str, db: AsyncSession) -> Optional[Dict]:
        result = await db.execute(select(PipelineJob).where(PipelineJob.id == job_id))
        job = result.scalar_one_or_none()
        if not job:
            return None
        return {
            "id": job.id,
            "status": job.status,
            "progress": job.progress,
            "result": job.result,
            "error": job.error,
            "started_at": job.started_at.isoformat() if job.started_at else None,
            "completed_at": job.completed_at.isoformat() if job.completed_at else None,
        }

    async def get_user_jobs(self, user_id: str, db: AsyncSession, limit: int = 10):
        result = await db.execute(
            select(PipelineJob)
            .where(PipelineJob.user_id == user_id)
            .order_by(PipelineJob.created_at.desc())
            .limit(limit)
        )
        jobs = result.scalars().all()
        return [
            {
                "id": j.id,
                "status": j.status,
                "job_type": j.job_type,
                "progress": j.progress,
                "created_at": j.created_at.isoformat() if j.created_at else None,
            }
            for j in jobs
        ]
