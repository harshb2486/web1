import uuid
from datetime import datetime, timezone
from sqlalchemy import String, Float, Integer, ForeignKey, DateTime, JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class TrendHistory(Base):
    __tablename__ = "trend_history"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), index=True, nullable=False)
    topic: Mapped[str] = mapped_column(String(255), nullable=False)
    growth_days: Mapped[int] = mapped_column(Integer, default=0)
    competition: Mapped[str] = mapped_column(String(50), default="Medium")
    fit: Mapped[int] = mapped_column(Integer, default=0)
    search_volume: Mapped[str] = mapped_column(String(50), default="")
    category: Mapped[str] = mapped_column(String(100), default="")
    direction: Mapped[str] = mapped_column(String(20), default="stable")
    captured_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

