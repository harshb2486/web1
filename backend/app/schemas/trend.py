from pydantic import BaseModel


class TrendResponse(BaseModel):
    id: str
    topic: str
    growthDays: int
    competition: str
    fit: int
    searchVolume: str
    category: str
    country: str
    direction: str
