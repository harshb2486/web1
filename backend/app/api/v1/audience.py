from fastapi import APIRouter, Depends

from app.core.security import get_current_user
from app.models.user import User
from app.schemas.audience import AudienceResponse
from app.services.seed import MOCK_AUDIENCE_DATA

router = APIRouter(tags=["audience"])


@router.get("/audience", response_model=AudienceResponse)
async def get_audience(current_user: User = Depends(get_current_user)):
    return AudienceResponse(**MOCK_AUDIENCE_DATA)
