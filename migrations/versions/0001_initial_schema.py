"""initial schema

Revision ID: 0001_initial_schema
Revises: 
Create Date: 2026-01-12
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision = "0001_initial_schema"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "channels",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("telegram_chat_id", sa.String(), nullable=False),
        sa.Column("disclaimer_text", sa.Text(), nullable=False, server_default=""),
        sa.Column("ingestion_enabled", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("telegram_chat_id", name="uq_channels__telegram_chat_id"),
    )

    op.create_table(
        "audit_events",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("event_type", sa.String(), nullable=False),
        sa.Column("event_ts", sa.DateTime(timezone=True), nullable=False),
        sa.Column("channel_id", sa.String(), sa.ForeignKey("channels.id"), nullable=True),
        sa.Column("correlation_id", sa.String(), nullable=False),
        sa.Column("payload_json", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default=sa.text("'{}'::jsonb")),
    )

    op.create_table(
        "messages",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("channel_id", sa.String(), nullable=False),
        sa.Column("message_id", sa.Integer(), nullable=False),
        sa.Column("sender_id", sa.String(), nullable=True),
        sa.Column("ts", sa.DateTime(timezone=True), nullable=False),
        sa.Column("text", sa.Text(), nullable=False, server_default=""),
        sa.Column("raw_json", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("deleted", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("quarantined", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("quarantine_reason", sa.String(), nullable=True),
        sa.Column("latest_version_ts", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("channel_id", "message_id", name="uq_messages__channel_id__message_id"),
    )

    op.create_table(
        "answers",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("channel_id", sa.String(), nullable=False),
        sa.Column("query_text", sa.Text(), nullable=False),
        sa.Column("cutoff_ts", sa.DateTime(timezone=True), nullable=False),
        sa.Column("recommendations_json", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default=sa.text("'[]'::jsonb")),
        sa.Column("telegram_message_id", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    op.create_table(
        "channel_daily_quota",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("channel_id", sa.String(), nullable=False),
        sa.Column("day_ist", sa.String(), nullable=False),
        sa.Column("questions_used", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("channel_id", "day_ist", name="uq_channel_daily_quota__channel_id__day_ist"),
    )

    op.create_table(
        "channel_cursors",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("channel_id", sa.String(), nullable=False),
        sa.Column("last_seen_message_id", sa.Integer(), nullable=True),
        sa.Column("last_seen_ts", sa.DateTime(timezone=True), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("channel_id", name="uq_channel_cursors__channel_id"),
    )


def downgrade() -> None:
    op.drop_table("channel_cursors")
    op.drop_table("channel_daily_quota")
    op.drop_table("answers")
    op.drop_table("messages")
    op.drop_table("audit_events")
    op.drop_table("channels")

