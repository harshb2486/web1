from pydantic import BaseModel


class CalendarSlotResponse(BaseModel):
    id: str
    day: str
    time: str
    score: int
    reason: str
    type: str
