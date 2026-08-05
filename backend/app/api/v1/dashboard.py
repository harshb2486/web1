from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.dashboard import DashboardStatsResponse

router = APIRouter(tags=["dashboard"])


@router.get("/dashboard", response_model=DashboardStatsResponse)
async def get_dashboard(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    profile = current_user.profile
    subscriber_count = profile.subscriber_count if profile else 284000
    sub_display = f"{subscriber_count // 1000}K" if subscriber_count >= 1000 else str(subscriber_count)

    return DashboardStatsResponse(
        totalViews="1.2M",
        revenue="$3,240",
        engagementRate="7.8%",
        subscribers=sub_display,
    )
