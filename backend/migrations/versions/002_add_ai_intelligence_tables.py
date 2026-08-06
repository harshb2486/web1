"""add_ai_intelligence_tables

Revision ID: 002
Revises: 001_initial
Create Date: 2025-01-01
"""
from alembic import op
import sqlalchemy as sa


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
        sa.Column("signal_type", sa.String(), nullable=False),
        sa.Column("title", sa.String(length=1024), nullable=True),
        sa.Column("text", sa.String(length=4096), nullable=True),
        sa.Column("url", sa.String(length=2048), nullable=True),
        sa.Column("metrics", JSON(), nullable=True),
        sa.Column("metadata", JSON(), nullable=True),
        sa.Column("collected_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("idx_raw_signals_user_source", "raw_signals", ["user_id", "source"])

    op.create_table(
        "processed_signals",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("user_id", sa.String(), nullable=False),
        sa.Column("raw_signal_id", sa.String(), nullable=False),
        sa.Column("keywords", JSON(), nullable=True),
        sa.Column("sentiment", sa.Float(), nullable=True),
        sa.Column("engagement_score", sa.Float(), nullable=True),
        sa.Column("performance_percentile", sa.Integer(), nullable=True),
        sa.Column("trend_direction", sa.String(length=20), nullable=True),
        sa.Column("trend_momentum", sa.Float(), nullable=True),
        sa.Column("metadata", JSON(), nullable=True),
        sa.Column("processed_at", sa.DateTime(timezone=True), nullable=False),
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
        sa.Column("computed_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("idx_feature_vectors_user", "feature_vectors", ["user_id"])

    op.create_table(
        "creator_memory",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("user_id", sa.String(), nullable=False),
        sa.Column("category", sa.String(length=100), nullable=False),
        sa.Column("key", sa.String(length=255), nullable=False),
        sa.Column("value", JSON(), nullable=False),
        sa.Column("confidence", sa.Float(), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("idx_creator_memory_user", "creator_memory", ["user_id"])

    op.create_table(
        "chat_messages",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("user_id", sa.String(), nullable=False),
        sa.Column("role", sa.String(length=20), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("intent", sa.String(length=100), nullable=True),
        sa.Column("tool_calls", JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("idx_chat_messages_user", "chat_messages", ["user_id"])

    op.create_table(
        "pipeline_jobs",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("user_id", sa.String(), nullable=False),
        sa.Column("job_type", sa.String(length=50), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("progress", sa.Integer(), nullable=True),
        sa.Column("result", JSON(), nullable=True),
        sa.Column("error", sa.Text(), nullable=True),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
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

