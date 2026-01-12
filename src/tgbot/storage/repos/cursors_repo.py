from __future__ import annotations

from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from tgbot.storage.models.channel_cursors import ChannelCursor


class CursorsRepo:
    def __init__(self, session: Session):
        self.session = session

    def get(self, channel_id: str) -> ChannelCursor | None:
        return self.session.scalar(select(ChannelCursor).where(ChannelCursor.channel_id == channel_id))

    def upsert(
        self, *, channel_id: str, last_seen_message_id: int | None, last_seen_ts: datetime | None
    ) -> ChannelCursor:
        cur = self.get(channel_id)
        if cur is None:
            cur = ChannelCursor(
                channel_id=channel_id, last_seen_message_id=last_seen_message_id, last_seen_ts=last_seen_ts
            )
            self.session.add(cur)
            self.session.flush()
            return cur

        cur.last_seen_message_id = last_seen_message_id
        cur.last_seen_ts = last_seen_ts
        self.session.add(cur)
        self.session.flush()
        return cur

