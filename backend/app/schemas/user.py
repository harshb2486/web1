from pydantic import BaseModel
from typing import Optional


class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    avatar: Optional[str] = None
    channel: str
    subscribers: int


class UpdateProfileRequest(BaseModel):
    name: Optional[str] = None
    channel: Optional[str] = None
    niche: Optional[str] = None
