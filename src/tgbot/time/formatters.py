from __future__ import annotations

from datetime import datetime

from tgbot.time.tz import to_ist


def format_ist_minute(dt_utc: datetime) -> str:
    dt = to_ist(dt_utc)
    return dt.strftime("%Y-%m-%d %H:%M")


def format_date_ist(dt_utc: datetime) -> str:
    dt = to_ist(dt_utc)
    return dt.strftime("%Y-%m-%d")

