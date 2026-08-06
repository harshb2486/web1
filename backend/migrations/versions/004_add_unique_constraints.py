"""add_unique_constraints

Revision ID: 004
Revises: 003
Create Date: 2025-01-01
"""
from alembic import op

revision = "004"
down_revision = "003"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_unique_constraint("uq_trend_user_topic", "trends", ["user_id", "topic"])
    op.create_unique_constraint("uq_recommendation_user_topic", "recommendations", ["user_id", "topic"])
    op.create_unique_constraint("uq_competitor_user_name", "competitors", ["user_id", "name"])


def downgrade() -> None:
    op.drop_constraint("uq_trend_user_topic", "trends")
    op.drop_constraint("uq_recommendation_user_topic", "recommendations")
    op.drop_constraint("uq_competitor_user_name", "competitors")

