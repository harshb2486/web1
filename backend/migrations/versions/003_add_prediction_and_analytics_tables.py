"""add_prediction_and_analytics_tables

Revision ID: 003
Revises: 002
Create Date: 2025-01-01
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB

revision = "003"
down_revision = "002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "predictions",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("user_id", sa.String(), nullable=False),
        sa.Column("topic", sa.String(), nullable=False),
        sa.Column("prediction_type", sa.String(), nullable=False),
        sa.Column("prediction", sa.Float(), nullable=False),
        sa.Column("confidence", sa.Float(), nullable=False),
        sa.Column("explanation", sa.Text(), nullable=True),
        sa.Column("range_min", sa.Float(), nullable=True),
        sa.Column("range_max", sa.Float(), nullable=True),
        sa.Column("risk", sa.String(), nullable=True),
        sa.Column("metadata", JSONB(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("idx_predictions_user", "predictions", ["user_id"])
    op.create_index("idx_predictions_topic", "predictions", ["topic"])
    op.create_index("idx_predictions_type", "predictions", ["prediction_type"])

    op.create_table(
        "trend_history",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("user_id", sa.String(), nullable=False),
        sa.Column("topic", sa.String(), nullable=False),
        sa.Column("growth_days", sa.Integer(), nullable=True),
        sa.Column("competition", sa.String(), nullable=True),
        sa.Column("fit", sa.Integer(), nullable=True),
        sa.Column("search_volume", sa.String(), nullable=True),
        sa.Column("category", sa.String(), nullable=True),
        sa.Column("direction", sa.String(), nullable=True),
        sa.Column("captured_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("idx_trend_history_user", "trend_history", ["user_id"])
    op.create_index("idx_trend_history_topic", "trend_history", ["topic"])
    op.create_index("idx_trend_history_captured", "trend_history", ["captured_at"])

    op.create_table(
        "competitor_history",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("user_id", sa.String(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("subscriber_count", sa.Integer(), nullable=True),
        sa.Column("growth_rate", sa.Float(), nullable=True),
        sa.Column("overlap", sa.Integer(), nullable=True),
        sa.Column("engagement_rate", sa.Float(), nullable=True),
        sa.Column("is_trending", sa.Boolean(), nullable=True),
        sa.Column("captured_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("idx_competitor_history_user", "competitor_history", ["user_id"])
    op.create_index("idx_competitor_history_name", "competitor_history", ["name"])
    op.create_index("idx_competitor_history_captured", "competitor_history", ["captured_at"])

    op.create_table(
        "analytics",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("user_id", sa.String(), nullable=False),
        sa.Column("metric_type", sa.String(), nullable=False),
        sa.Column("period", sa.String(), nullable=False),
        sa.Column("value", sa.Float(), nullable=True),
        sa.Column("breakdown", JSONB(), nullable=True),
        sa.Column("computed_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("idx_analytics_user", "analytics", ["user_id"])
    op.create_index("idx_analytics_type", "analytics", ["metric_type"])
    op.create_index("idx_analytics_period", "analytics", ["period"])

    op.create_table(
        "embeddings",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("user_id", sa.String(), nullable=False),
        sa.Column("entity_type", sa.String(), nullable=False),
        sa.Column("entity_id", sa.String(), nullable=False),
        sa.Column("text", sa.String(), nullable=False),
        sa.Column("vector", JSONB(), nullable=False),
        sa.Column("dimension", sa.Integer(), nullable=True),
        sa.Column("metadata", JSONB(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("idx_embeddings_user", "embeddings", ["user_id"])
    op.create_index("idx_embeddings_entity_type", "embeddings", ["entity_type"])
    op.create_index("idx_embeddings_entity_id", "embeddings", ["entity_id"])


def downgrade() -> None:
    op.drop_table("embeddings")
    op.drop_table("analytics")
    op.drop_table("competitor_history")
    op.drop_table("trend_history")
    op.drop_table("predictions")
