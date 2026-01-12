from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from tgbot.storage.db import Base, utc_now


class ChannelDailyQuota(Base):
    __tablename__ = "channel_daily_quota"
    __table_args__ = (
        UniqueConstraint("channel_id", "day_ist", name="uq_channel_daily_quota__channel_id__day_ist"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    channel_id: Mapped[str] = mapped_column(String, nullable=False)
    # YYYY-MM-DD in IST
    day_ist: Mapped[str] = mapped_column(String, nullable=False)

    questions_used: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=utc_now, onupdate=utc_now
    )

