from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.ai.resolver import DataSourceResolver

router = APIRouter(tags=["recommendations"])


@router.get("/recommendations")
async def get_recommendations(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    resolver = DataSourceResolver(db, current_user.id)
    recs = await resolver.get_recommendations()
    return recs
