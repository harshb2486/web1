from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.ai.resolver import DataSourceResolver
from app.api.v1.response import success_response

router = APIRouter(tags=["opportunities"])


@router.get("/opportunities")
async def get_opportunities(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    resolver = DataSourceResolver(db, current_user.id)
    trends = await resolver.get_trends()
    recommendations = await resolver.get_recommendations()

    opportunities = []
    for t in trends:
        matching_recs = [r for r in recommendations if r.get("category") == t.get("category")]
        best_rec = max(matching_recs, key=lambda r: r.get("confidence", 0)) if matching_recs else None

        opportunities.append({
            "topic": t.get("topic"),
            "score": t.get("fit", 0),
            "trend": {
                "direction": t.get("direction"),
                "searchVolume": t.get("searchVolume"),
                "growthDays": t.get("growthDays"),
            },
            "recommendation": {
                "confidence": best_rec.get("confidence") if best_rec else None,
                "expectedViews": best_rec.get("expectedViews") if best_rec else None,
                "potential": best_rec.get("potential") if best_rec else None,
            } if best_rec else None,
            "category": t.get("category"),
        })

    opportunities.sort(key=lambda x: x["score"], reverse=True)
    return success_response(opportunities[:10])
