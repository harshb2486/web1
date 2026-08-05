from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.ai.resolver import DataSourceResolver

router = APIRouter(tags=["competitors"])


@router.get("/competitors")
async def get_competitors(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    resolver = DataSourceResolver(db, current_user.id)
    competitors = await resolver.get_competitors()
    return competitors
