from fastapi import APIRouter, Depends

from app.core.security import get_current_user
from app.models.user import User
from app.schemas.revenue import RevenueResponse
from app.services.seed import MOCK_REVENUE_DATA

router = APIRouter(tags=["revenue"])


@router.get("/revenue", response_model=RevenueResponse)
async def get_revenue(current_user: User = Depends(get_current_user)):
    return RevenueResponse(**MOCK_REVENUE_DATA)
