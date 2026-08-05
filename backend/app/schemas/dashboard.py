from pydantic import BaseModel
from typing import List


class DashboardStatsResponse(BaseModel):
    totalViews: str
    revenue: str
    engagementRate: str
    subscribers: str
