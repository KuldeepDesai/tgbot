from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from tgbot.storage.db import Base, utc_now


class Channel(Base):
    __tablename__ = "channels"
    __table_args__ = (UniqueConstraint("telegram_chat_id", name="uq_channels__telegram_chat_id"),)

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    telegram_chat_id: Mapped[str] = mapped_column(String, nullable=False)
    disclaimer_text: Mapped[str] = mapped_column(Text, nullable=False, default="")

    ingestion_enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=utc_now, onupdate=utc_now
    )

