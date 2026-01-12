from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from tgbot.storage.db import Base, utc_now


class Message(Base):
    __tablename__ = "messages"
    __table_args__ = (UniqueConstraint("channel_id", "message_id", name="uq_messages__channel_id__message_id"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    channel_id: Mapped[str] = mapped_column(String, nullable=False)
    message_id: Mapped[int] = mapped_column(Integer, nullable=False)

    sender_id: Mapped[str | None] = mapped_column(String, nullable=True)
    ts: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    text: Mapped[str] = mapped_column(Text, nullable=False, default="")
    raw_json: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)

    deleted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    quarantined: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    quarantine_reason: Mapped[str | None] = mapped_column(String, nullable=True)

    latest_version_ts: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=utc_now)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=utc_now, onupdate=utc_now
    )

