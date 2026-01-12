from __future__ import annotations

from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from tgbot.storage.models.quota import ChannelDailyQuota
from tgbot.time.tz import IST


class QuotaRepo:
    def __init__(self, session: Session):
        self.session = session

    @staticmethod
    def _day_ist(now_utc: datetime) -> str:
        return now_utc.astimezone(IST).strftime("%Y-%m-%d")

    def get_or_create(self, *, channel_id: str, now_utc: datetime) -> ChannelDailyQuota:
        day = self._day_ist(now_utc)
        row = self.session.scalar(
            select(ChannelDailyQuota)
            .where(ChannelDailyQuota.channel_id == channel_id)
            .where(ChannelDailyQuota.day_ist == day)
        )
        if row is None:
            row = ChannelDailyQuota(channel_id=channel_id, day_ist=day, questions_used=0)
            self.session.add(row)
            self.session.flush()
        return row

    def try_consume_question(
        self, *, channel_id: str, now_utc: datetime, daily_limit: int
    ) -> tuple[bool, int]:
        """
        Returns (allowed, remaining_after_attempt_if_allowed_else_current_remaining).
        """
        row = self.get_or_create(channel_id=channel_id, now_utc=now_utc)
        if row.questions_used + 1 > daily_limit:
            return False, max(0, daily_limit - row.questions_used)
        row.questions_used += 1
        self.session.add(row)
        self.session.flush()
        return True, max(0, daily_limit - row.questions_used)

