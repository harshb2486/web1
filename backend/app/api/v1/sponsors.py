from fastapi import APIRouter, Depends

from app.core.security import get_current_user
from app.models.user import User
from app.schemas.sponsor import SponsorResponse
from app.services.seed import MOCK_SPONSORS

router = APIRouter(tags=["sponsors"])


@router.get("/sponsors", response_model=list[SponsorResponse])
async def get_sponsors(current_user: User = Depends(get_current_user)):
    return [SponsorResponse(id=str(i + 1), **s) for i, s in enumerate(MOCK_SPONSORS)]
