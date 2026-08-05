from pydantic import BaseModel
from typing import List


class OnboardingRequest(BaseModel):
    creatorType: str
    platforms: List[str]
    goals: List[str]
    niche: str
    theme: str = "dark"
