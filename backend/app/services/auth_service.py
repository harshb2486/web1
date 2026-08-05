from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_password_hash, create_access_token, create_refresh_token, decode_token
from app.models.user import User
from app.models.profile import CreatorProfile
from app.models.settings import UserSettings
from app.schemas.auth import SignupRequest, LoginRequest, TokenResponse
from app.services.seed import seed_user_data


async def signup(data: SignupRequest, db: AsyncSession) -> TokenResponse:
    from sqlalchemy import select
    result = await db.execute(select(User).where(User.email == data.email))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    user = User(email=data.email, hashed_password=get_password_hash(data.password))
    db.add(user)
    await db.flush()

    profile = CreatorProfile(user_id=user.id, name=data.name, channel_name=data.name, subscriber_count=0)
    db.add(profile)

    settings = UserSettings(user_id=user.id)
    db.add(settings)

    await db.flush()
    await seed_user_data(db, user.id)

    access_token = create_access_token({"sub": user.id})
    refresh_token = create_refresh_token({"sub": user.id})
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


async def login(data: LoginRequest, db: AsyncSession) -> TokenResponse:
    from sqlalchemy import select
    from app.core.security import verify_password

    result = await db.execute(select(User).where(User.email == data.email))
    user = result.scalar_one_or_none()
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

    access_token = create_access_token({"sub": user.id})
    refresh_token = create_refresh_token({"sub": user.id})
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


async def refresh_token(refresh_token_str: str, db: AsyncSession) -> TokenResponse:
    from sqlalchemy import select

    payload = decode_token(refresh_token_str)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

    user_id = payload.get("sub")
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    access_token = create_access_token({"sub": user.id})
    new_refresh_token = create_refresh_token({"sub": user.id})
    return TokenResponse(access_token=access_token, refresh_token=new_refresh_token)
