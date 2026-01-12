from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from tgbot.storage.db import Base, utc_now


class Answer(Base):
    __tablename__ = "answers"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    channel_id: Mapped[str] = mapped_column(String, nullable=False)

    query_text: Mapped[str] = mapped_column(Text, nullable=False)
    cutoff_ts: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    # Cached recommendations for pagination/idempotency:
    # list[{ provider_key, title, citations:[{...}], contacts:[...], stance }]
    recommendations_json: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)

    # Telegram message id of the bot's answer (for feedback linking; optional)
    telegram_message_id: Mapped[int | None] = mapped_column(Integer, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=utc_now)

