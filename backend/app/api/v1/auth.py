from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user
from app.schemas.auth import (
    SignupRequest, LoginRequest, TokenResponse, RefreshRequest,
    ForgotPasswordRequest, ResetPasswordRequest,
)
from app.services.auth_service import signup, login, refresh_token
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def signup_handler(data: SignupRequest, db: AsyncSession = Depends(get_db)):
    return await signup(data, db)


@router.post("/login", response_model=TokenResponse)
async def login_handler(data: LoginRequest, db: AsyncSession = Depends(get_db)):
    return await login(data, db)


@router.post("/refresh", response_model=TokenResponse)
async def refresh_handler(data: RefreshRequest, db: AsyncSession = Depends(get_db)):
    return await refresh_token(data.refresh_token, db)


@router.post("/logout")
async def logout_handler():
    return {"message": "Logged out"}


@router.post("/forgot-password")
async def forgot_password_handler(data: ForgotPasswordRequest):
    return {"message": "If the email exists, a reset link has been sent"}


@router.post("/reset-password")
async def reset_password_handler(data: ResetPasswordRequest):
    return {"message": "Password has been reset"}
