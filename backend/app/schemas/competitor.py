from pydantic import BaseModel


class CompetitorResponse(BaseModel):
    id: str
    name: str
    subscribers: int
    growthRate: float
    overlap: int
    engagement: float
    lastVideo: str
    lastVideoViews: int
    trending: bool
