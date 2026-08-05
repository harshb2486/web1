from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.ai.prediction.service import PredictionService
from app.ai.memory.service import MemoryService
from app.api.v1.response import success_response

router = APIRouter(tags=["analyze"])
prediction_service = PredictionService()
memory_service = MemoryService()


class AnalyzeRequest(BaseModel):
    topic: str
    title: str = ""
    description: str = ""


@router.post("/analyze")
async def analyze_topic(
    data: AnalyzeRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    trend_data = {"raw_momentum": 0.7, "competition": "Medium", "fit": 70}
    view_pred = await prediction_service.predict_video(data.topic, trend_data, current_user.id, db)
    rev_pred = await prediction_service.predict_revenue(
        view_pred.views.range.min, view_pred.views.range.max, current_user.id, db
    )
    memory = await memory_service.get_full_memory(current_user.id, db)

    result = {
        "topic": data.topic,
        "analysis": {
            "views": view_pred.views.model_dump(),
            "ctr": view_pred.ctr.model_dump(),
            "retention": view_pred.retention.model_dump(),
            "revenue": rev_pred.revenue.model_dump(),
        },
        "context": {
            "niche": memory.creator_profile.niche,
            "successful_topics": [t.topic for t in memory.learning_history.successful_topics[:3]],
            "preferred_categories": memory.preferences.categories[:3],
        },
    }
    return success_response(result)
