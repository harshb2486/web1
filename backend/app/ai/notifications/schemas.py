from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class NotificationCreate(BaseModel):
    type: str
    priority: str = "medium"
    title: str
    message: str
    metadata: dict = {}


class NotificationResponse(BaseModel):
    id: str
    type: str
    priority: str
    title: str
    message: str
    read: bool
    created_at: Optional[datetime] = None
    metadata: dict = {}


class NotificationRule(BaseModel):
    name: str
    check_type: str
    threshold: float = 0.0
    notification_type: str
    priority: str = "medium"
    template: str
