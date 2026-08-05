from pydantic import BaseModel
from typing import List


class RevenueBreakdown(BaseModel):
    ads: int
    sponsorships: int
    affiliate: int
    membership: int


class MonthlyRevenue(BaseModel):
    month: str
    revenue: int
    ads: int
    sponsors: int


class RevenueChartPoint(BaseModel):
    month: str
    revenue: int


class RevenueResponse(BaseModel):
    current: int
    breakdown: RevenueBreakdown
    monthly: List[MonthlyRevenue]
    chartData: List[RevenueChartPoint]
