from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.video import Video
from app.models.feature_vector import FeatureVector
from app.models.profile import CreatorProfile
from app.schemas.dashboard import DashboardStatsResponse

router = APIRouter(tags=["dashboard"])


@router.get("/dashboard", response_model=DashboardStatsResponse)
async def get_dashboard(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    videos_result = await db.execute(select(Video).where(Video.user_id == current_user.id))
    videos = videos_result.scalars().all()

    total_views = sum(v.views for v in videos) if videos else 0
    total_revenue = sum(v.revenue for v in videos) if videos else 0

    if total_views >= 1_000_000:
        views_display = f"{total_views / 1_000_000:.1f}M"
    elif total_views >= 1_000:
        views_display = f"{total_views / 1_000:.0f}K"
    else:
        views_display = str(total_views)

    revenue_display = f"${total_revenue:,.0f}"

    features_result = await db.execute(select(FeatureVector).where(FeatureVector.user_id == current_user.id))
    features = features_result.scalar_one_or_none()

    engagement_rate = f"{features.engagement_score:.1f}%" if features else "5.0%"

    profile_result = await db.execute(select(CreatorProfile).where(CreatorProfile.user_id == current_user.id))
    profile = profile_result.scalar_one_or_none()

    subscriber_count = profile.subscriber_count if profile else 0
    if subscriber_count >= 1_000_000:
        sub_display = f"{subscriber_count / 1_000_000:.1f}M"
    elif subscriber_count >= 1_000:
        sub_display = f"{subscriber_count / 1_000:.0f}K"
    else:
        sub_display = str(subscriber_count)

    return DashboardStatsResponse(
        totalViews=views_display,
        revenue=revenue_display,
        engagementRate=engagement_rate,
        subscribers=sub_display,
    )
