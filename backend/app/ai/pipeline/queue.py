from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.pipeline_job import PipelineJob


class PipelineQueue:
    async def enqueue(self, user_id: str, job_type: str, db: AsyncSession) -> PipelineJob:
        job = PipelineJob(
            user_id=user_id,
            job_type=job_type,
            status="queued",
        )
        db.add(job)
        await db.flush()
        return job

    async def start_job(self, job: PipelineJob, db: AsyncSession) -> None:
        job.status = "running"
        job.started_at = datetime.now(timezone.utc)
        await db.flush()

    async def complete_job(self, job: PipelineJob, result: dict, db: AsyncSession) -> None:
        job.status = "completed"
        job.progress = 100
        job.result = result
        job.completed_at = datetime.now(timezone.utc)
        await db.flush()

    async def fail_job(self, job: PipelineJob, error: str, db: AsyncSession) -> None:
        job.status = "failed"
        job.error = error
        job.completed_at = datetime.now(timezone.utc)
        await db.flush()

    async def get_job(self, job_id: str, db: AsyncSession) -> PipelineJob | None:
        result = await db.execute(select(PipelineJob).where(PipelineJob.id == job_id))
        return result.scalar_one_or_none()

    async def get_user_jobs(self, user_id: str, db: AsyncSession, limit: int = 10):
        result = await db.execute(
            select(PipelineJob)
            .where(PipelineJob.user_id == user_id)
            .order_by(PipelineJob.created_at.desc())
            .limit(limit)
        )
        return result.scalars().all()
