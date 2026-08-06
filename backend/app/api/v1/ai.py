from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.jobs.orchestrator import JobOrchestrator
from app.ai.features.feature_engine import FeatureEngine
from app.ai.engines.prediction_engine import PredictionEngine
from app.ai.engines.creator_memory import CreatorMemoryStore
from app.api.v1.response import success_response

router = APIRouter(prefix="/ai", tags=["ai"])
orchestrator = JobOrchestrator()
feature_engine = FeatureEngine()
prediction_engine = PredictionEngine()
memory_store = CreatorMemoryStore()


class PredictRequest(BaseModel):
    topic: str


@router.post("/run-pipeline")
async def run_pipeline(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    job_id = await orchestrator.run_pipeline(current_user.id, db)
    return success_response({"job_id": job_id, "status": "queued"})


@router.get("/pipeline/status/{job_id}")
async def get_pipeline_status(
    job_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    status = await orchestrator.get_status(job_id, db)
    if not status:
        raise HTTPException(status_code=404, detail="Job not found")
    return success_response(status)


@router.get("/pipeline/jobs")
async def get_pipeline_jobs(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    jobs = await orchestrator.get_user_jobs(current_user.id, db)
    return success_response(jobs)


@router.post("/compute-features")
async def compute_features(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    vector = await feature_engine.compute_all(current_user.id, db)
    return success_response({
        "ctr": vector.ctr,
        "avg_watch_time": vector.avg_watch_time,
        "growth_pct": vector.growth_pct,
        "retention_rate": vector.retention_rate,
        "upload_frequency": vector.upload_frequency,
        "view_velocity": vector.view_velocity,
        "engagement_score": vector.engagement_score,
        "trend_score": vector.trend_score,
        "competition_score": vector.competition_score,
    })


@router.get("/features")
async def get_features(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    from sqlalchemy import select
    from app.models.feature_vector import FeatureVector
    result = await db.execute(select(FeatureVector).where(FeatureVector.user_id == current_user.id))
    vector = result.scalar_one_or_none()
    if not vector:
        return success_response({"computed": False})
    return success_response({
        "computed": True,
        "ctr": vector.ctr,
        "avg_watch_time": vector.avg_watch_time,
        "growth_pct": vector.growth_pct,
        "retention_rate": vector.retention_rate,
        "upload_frequency": vector.upload_frequency,
        "view_velocity": vector.view_velocity,
        "engagement_score": vector.engagement_score,
        "trend_score": vector.trend_score,
        "competition_score": vector.competition_score,
        "computed_at": vector.computed_at.isoformat() if vector.computed_at else None,
    })


@router.post("/predict")
async def predict(
    data: PredictRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    views = await prediction_engine.predict_views(data.topic, current_user.id, db)
    revenue = await prediction_engine.predict_revenue(views["low"], views["high"], current_user.id, db)
    return success_response({"topic": data.topic, "views": views, "revenue": revenue})


@router.get("/memory")
async def get_memory(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    prefs = await memory_store.get_preferences(current_user.id, db)
    return success_response(prefs)
