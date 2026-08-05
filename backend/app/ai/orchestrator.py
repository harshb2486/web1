from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.pipeline.queue import PipelineQueue
from app.ai.pipeline.workers.pipeline_worker import PipelineWorker
from app.models.pipeline_job import PipelineJob


class Orchestrator:
    def __init__(self):
        self.queue = PipelineQueue()
        self.worker = PipelineWorker()

    async def run(self, user_id: str, db: AsyncSession) -> dict:
        job = await self.queue.enqueue(user_id, "full", db)
        await self.queue.start_job(job, db)

        try:
            result = await self.worker.run_full_pipeline(user_id, db)
            await self.queue.complete_job(job, result, db)
            return {"job_id": job.id, "status": "completed", "result": result}
        except Exception as e:
            await self.queue.fail_job(job, str(e), db)
            return {"job_id": job.id, "status": "failed", "error": str(e)}

    async def get_status(self, job_id: str, db: AsyncSession):
        job = await self.queue.get_job(job_id, db)
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

    async def get_user_jobs(self, user_id: str, db: AsyncSession):
        jobs = await self.queue.get_user_jobs(user_id, db)
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
