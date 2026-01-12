from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from tgbot.storage.db import Base, utc_now


class ChannelCursor(Base):
    __tablename__ = "channel_cursors"
    __table_args__ = (UniqueConstraint("channel_id", name="uq_channel_cursors__channel_id"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    channel_id: Mapped[str] = mapped_column(String, nullable=False)

    last_seen_message_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    last_seen_ts: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=utc_now, onupdate=utc_now)

