"""add_ai_intelligence_tables

Revision ID: 002
Revises: 001_initial
Create Date: 2025-01-01
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSONB

revision = "002"
down_revision = "001_initial"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "raw_signals",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("user_id", sa.String(), nullable=False),
        sa.Column("source", sa.String(), nullable=False),
        sa.Column("external_id", sa.String(), nullable=True),
        sa.Column("title", sa.String(), nullable=True),
        sa.Column("text", sa.Text(), nullable=True),
        sa.Column("url", sa.String(), nullable=True),
        sa.Column("author", sa.String(), nullable=True),
        sa.Column("published_at", sa.DateTime(), nullable=True),
        sa.Column("collected_at", sa.DateTime(), nullable=False),
        sa.Column("metrics", JSONB(), nullable=True),
        sa.Column("metadata", JSONB(), nullable=True),
        sa.Column("raw_data", JSONB(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("idx_raw_signals_user_source", "raw_signals", ["user_id", "source"])
    op.create_index("idx_raw_signals_published", "raw_signals", ["published_at"])

    op.create_table(
        "processed_signals",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("raw_signal_id", sa.String(), nullable=False),
        sa.Column("user_id", sa.String(), nullable=False),
        sa.Column("processed_text", sa.Text(), nullable=True),
        sa.Column("keywords", JSONB(), nullable=True),
        sa.Column("sentiment", sa.Float(), nullable=True),
        sa.Column("categories", JSONB(), nullable=True),
        sa.Column("quality_score", sa.Float(), nullable=True),
        sa.Column("engagement_score", sa.Float(), nullable=True),
        sa.Column("trend_score", sa.Float(), nullable=True),
        sa.Column("features", JSONB(), nullable=True),
        sa.Column("processed_at", sa.DateTime(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("idx_processed_signals_user", "processed_signals", ["user_id"])
    op.create_foreign_key("fk_processed_raw", "processed_signals", "raw_signals", ["raw_signal_id"], ["id"])

    op.create_table(
        "feature_vectors",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("user_id", sa.String(), nullable=False),
        sa.Column("ctr", sa.Float(), nullable=True),
        sa.Column("avg_watch_time", sa.Float(), nullable=True),
        sa.Column("growth_pct", sa.Float(), nullable=True),
        sa.Column("retention_rate", sa.Float(), nullable=True),
        sa.Column("upload_frequency", sa.Float(), nullable=True),
        sa.Column("view_velocity", sa.Float(), nullable=True),
        sa.Column("engagement_score", sa.Float(), nullable=True),
        sa.Column("trend_score", sa.Float(), nullable=True),
        sa.Column("competition_score", sa.Float(), nullable=True),
        sa.Column("computed_at", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("idx_feature_vectors_user", "feature_vectors", ["user_id"])

    op.create_table(
        "creator_memory",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("user_id", sa.String(), nullable=False),
        sa.Column("category", sa.String(), nullable=False),
        sa.Column("key", sa.String(), nullable=False),
        sa.Column("value", JSONB(), nullable=False),
        sa.Column("weight", sa.Float(), nullable=False),
        sa.Column("last_updated", sa.DateTime(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("idx_creator_memory_user", "creator_memory", ["user_id"])

    op.create_table(
        "chat_messages",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("user_id", sa.String(), nullable=False),
        sa.Column("role", sa.String(), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("intent", sa.String(), nullable=True),
        sa.Column("tool_calls", JSONB(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("idx_chat_messages_user", "chat_messages", ["user_id"])

    op.create_table(
        "pipeline_jobs",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("user_id", sa.String(), nullable=False),
        sa.Column("job_type", sa.String(), nullable=False),
        sa.Column("status", sa.String(), nullable=False),
        sa.Column("progress", sa.Integer(), nullable=False),
        sa.Column("result", JSONB(), nullable=True),
        sa.Column("error", sa.Text(), nullable=True),
        sa.Column("started_at", sa.DateTime(), nullable=True),
        sa.Column("completed_at", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("idx_pipeline_jobs_user", "pipeline_jobs", ["user_id"])
    op.create_index("idx_pipeline_jobs_status", "pipeline_jobs", ["status"])


def downgrade() -> None:
    op.drop_table("pipeline_jobs")
    op.drop_table("chat_messages")
    op.drop_table("creator_memory")
    op.drop_table("feature_vectors")
    op.drop_table("processed_signals")
    op.drop_table("raw_signals")
