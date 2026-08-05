from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.calendar_event import CalendarEvent
from app.schemas.calendar import CalendarSlotResponse

router = APIRouter(tags=["calendar"])


@router.get("/calendar", response_model=list[CalendarSlotResponse])
async def get_calendar(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(CalendarEvent).where(CalendarEvent.user_id == current_user.id)
    )
    events = result.scalars().all()
    return [
        CalendarSlotResponse(
            id=e.id,
            day=e.day,
            time=e.time,
            score=e.score,
            reason=e.reason,
            type=e.type,
        )
        for e in events
    ]
