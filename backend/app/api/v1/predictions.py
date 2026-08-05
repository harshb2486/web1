from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.ai.prediction.service import PredictionService
from app.ai.prediction.schemas import SimulateRequest
from app.api.v1.response import success_response

router = APIRouter(tags=["predictions"])
prediction_service = PredictionService()


@router.get("/predictions")
async def get_predictions(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    from sqlalchemy import select
    from app.models.prediction import Prediction
    result = await db.execute(
        select(Prediction).where(Prediction.user_id == current_user.id)
    )
    preds = result.scalars().all()
    data = [
        {
            "id": p.id,
            "topic": p.topic,
            "prediction_type": p.prediction_type,
            "prediction": p.prediction,
            "confidence": p.confidence,
            "explanation": p.explanation,
            "range": {"min": p.range_min, "max": p.range_max},
            "risk": p.risk,
            "created_at": p.created_at.isoformat() if p.created_at else None,
        }
        for p in preds
    ]
    return success_response(data)


@router.post("/predict")
async def predict(
    data: SimulateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    trend_data = {"raw_momentum": 0.7, "competition": "Medium", "fit": 70}
    view_pred = await prediction_service.predict_video(data.topic, trend_data, current_user.id, db)
    rev_pred = await prediction_service.predict_revenue(
        view_pred.views.range.min, view_pred.views.range.max, current_user.id, db
    )
    result = {
        "topic": data.topic,
        "views": view_pred.views.model_dump(),
        "ctr": view_pred.ctr.model_dump(),
        "retention": view_pred.retention.model_dump(),
        "revenue": rev_pred.model_dump(),
    }
    return success_response(result)


@router.post("/simulate")
async def simulate(
    data: SimulateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await prediction_service.simulate(data.topic, current_user.id, db)
    return success_response(result.model_dump())
