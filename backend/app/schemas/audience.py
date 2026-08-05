from pydantic import BaseModel
from typing import List


class AgeDistribution(BaseModel):
    range: str
    percent: int


class CountryDistribution(BaseModel):
    name: str
    percent: int


class DeviceDistribution(BaseModel):
    name: str
    percent: int


class AudienceResponse(BaseModel):
    age: List[AgeDistribution]
    countries: List[CountryDistribution]
    devices: List[DeviceDistribution]
    returningViewers: int
    avgWatchTime: str
    peakHours: List[str]
    insight: str
