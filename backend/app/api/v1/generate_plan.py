from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.jobs.orchestrator import JobOrchestrator
from app.api.v1.response import success_response

router = APIRouter(tags=["generate-plan"])
orchestrator = JobOrchestrator()


class GeneratePlanRequest(BaseModel):
    goals: str = "increase views and engagement"
    timeframe: str = "30 days"


@router.post("/generate-plan")
async def generate_plan(
    data: GeneratePlanRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    from app.ai.resolver import DataSourceResolver
    resolver = DataSourceResolver(db, current_user.id)
    trends = await resolver.get_trends()
    recommendations = await resolver.get_recommendations()

    plan = {
        "goals": data.goals,
        "timeframe": data.timeframe,
        "content_plan": [
            {
                "week": i + 1,
                "topic": rec.get("topic", ""),
                "category": rec.get("category", ""),
                "expected_views": rec.get("expectedViews", {}),
                "publish_time": rec.get("publishTime", ""),
                "confidence": rec.get("confidence", 0),
            }
            for i, rec in enumerate(recommendations[:4])
        ],
        "trends_to_watch": [
            {
                "topic": t.get("topic", ""),
                "direction": t.get("direction", ""),
                "fit": t.get("fit", 0),
            }
            for t in trends[:5]
        ],
        "actions": [
            "Post 2-3 times per week during peak hours",
            "Focus on trending topics in your niche",
            "Monitor competitor activity for content gaps",
            "Engage with audience in comments within 1 hour of posting",
        ],
    }
    return success_response(plan)
