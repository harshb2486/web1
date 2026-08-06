import uuid
from datetime import datetime, timezone
from sqlalchemy import String, Integer, Float, ForeignKey, DateTime, JSON, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Recommendation(Base):
    __tablename__ = "recommendations"
    __table_args__ = (
        UniqueConstraint("user_id", "topic", name="uq_recommendation_user_topic"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), nullable=False)
    topic: Mapped[str] = mapped_column(String(255), nullable=False)
    confidence: Mapped[int] = mapped_column(Integer, nullable=False)
    evidence: Mapped[list] = mapped_column(JSON, default=list)
    expected_views_low: Mapped[int] = mapped_column(Integer, default=0)
    expected_views_high: Mapped[int] = mapped_column(Integer, default=0)
    expected_revenue_low: Mapped[int] = mapped_column(Integer, default=0)
    expected_revenue_high: Mapped[int] = mapped_column(Integer, default=0)
    risks: Mapped[list] = mapped_column(JSON, default=list)
    similar_content_title: Mapped[str] = mapped_column(String(512), default="")
    similar_content_views: Mapped[int] = mapped_column(Integer, default=0)
    publish_time: Mapped[str] = mapped_column(String(100), default="")
    category: Mapped[str] = mapped_column(String(100), default="")
    potential: Mapped[str] = mapped_column(String(20), default="medium")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="recommendations")

