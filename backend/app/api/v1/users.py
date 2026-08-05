from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.profile import CreatorProfile
from app.schemas.user import UserResponse, UpdateProfileRequest

router = APIRouter(tags=["users"])


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    profile = current_user.profile
    return UserResponse(
        id=current_user.id,
        name=profile.name if profile else current_user.email.split("@")[0],
        email=current_user.email,
        avatar=profile.avatar_url if profile else None,
        channel=profile.channel_name if profile else "",
        subscribers=profile.subscriber_count if profile else 0,
    )


@router.put("/profile", response_model=UserResponse)
async def update_profile(
    data: UpdateProfileRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    profile = current_user.profile
    if not profile:
        profile = CreatorProfile(user_id=current_user.id, name="", channel_name="")
        db.add(profile)
        await db.flush()

    if data.name is not None:
        profile.name = data.name
    if data.channel is not None:
        profile.channel_name = data.channel
    if data.niche is not None:
        profile.niche = data.niche

    await db.flush()

    return UserResponse(
        id=current_user.id,
        name=profile.name,
        email=current_user.email,
        avatar=profile.avatar_url,
        channel=profile.channel_name,
        subscribers=profile.subscriber_count,
    )
