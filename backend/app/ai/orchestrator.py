from app.jobs.orchestrator import JobOrchestrator


class Orchestrator:
    def __init__(self):
        self._job_orchestrator = JobOrchestrator()

    async def run(self, user_id: str, db):
        return await self._job_orchestrator.run_pipeline(user_id, db)

    async def get_status(self, job_id: str, db):
        return await self._job_orchestrator.get_status(job_id, db)

    async def get_user_jobs(self, user_id: str, db):
        return await self._job_orchestrator.get_user_jobs(user_id, db)
