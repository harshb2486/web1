import uuid
from datetime import datetime, timezone
from sqlalchemy import String, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    profile = relationship("CreatorProfile", back_populates="user", uselist=False, lazy="selectin")
    notifications = relationship("Notification", back_populates="user", lazy="selectin")
    recommendations = relationship("Recommendation", back_populates="user", lazy="selectin")
    trends = relationship("Trend", back_populates="user", lazy="selectin")
    competitors = relationship("Competitor", back_populates="user", lazy="selectin")
    calendar_events = relationship("CalendarEvent", back_populates="user", lazy="selectin")
    settings = relationship("UserSettings", back_populates="user", uselist=False, lazy="selectin")
