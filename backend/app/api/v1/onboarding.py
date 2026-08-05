from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.profile import CreatorProfile
from app.models.settings import UserSettings
from app.schemas.onboarding import OnboardingRequest

router = APIRouter(tags=["onboarding"])


@router.post("/onboarding")
async def complete_onboarding(
    data: OnboardingRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    profile = current_user.profile
    if not profile:
        profile = CreatorProfile(user_id=current_user.id, name=current_user.email.split("@")[0], channel_name="")
        db.add(profile)

    profile.creator_type = data.creatorType
    profile.niche = data.niche

    settings = current_user.settings
    if not settings:
        settings = UserSettings(user_id=current_user.id)
        db.add(settings)
    settings.dark_mode = data.theme

    await db.flush()
    return {"message": "Onboarding completed"}
