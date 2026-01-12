from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from tgbot.storage.db import Base, utc_now


class AuditEvent(Base):
    __tablename__ = "audit_events"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    event_type: Mapped[str] = mapped_column(String, nullable=False)
    event_ts: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=utc_now)

    channel_id: Mapped[str | None] = mapped_column(String, ForeignKey("channels.id"), nullable=True)
    correlation_id: Mapped[str] = mapped_column(String, nullable=False)

    payload_json: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)

