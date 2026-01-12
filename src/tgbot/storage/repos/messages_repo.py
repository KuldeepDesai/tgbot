from __future__ import annotations

from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from tgbot.storage.models.messages import Message


class MessagesRepo:
    def __init__(self, session: Session):
        self.session = session

    def upsert_latest(
        self,
        *,
        channel_id: str,
        message_id: int,
        ts: datetime,
        text: str,
        raw_json: dict,
        version_ts: datetime,
        sender_id: str | None = None,
        quarantined: bool = False,
        quarantine_reason: str | None = None,
    ) -> Message:
        msg = self.session.scalar(
            select(Message).where(Message.channel_id == channel_id).where(Message.message_id == message_id)
        )
        if msg is None:
            msg = Message(
                channel_id=channel_id,
                message_id=message_id,
                sender_id=sender_id,
                ts=ts,
                text=text,
                raw_json=raw_json,
                deleted=False,
                quarantined=quarantined,
                quarantine_reason=quarantine_reason,
                latest_version_ts=version_ts,
            )
            self.session.add(msg)
            self.session.flush()
            return msg

        # Latest-wins semantics: apply only if newer.
        if version_ts >= msg.latest_version_ts:
            msg.sender_id = sender_id
            msg.ts = ts
            msg.text = text
            msg.raw_json = raw_json
            msg.deleted = False
            msg.quarantined = quarantined
            msg.quarantine_reason = quarantine_reason
            msg.latest_version_ts = version_ts
            self.session.add(msg)
            self.session.flush()
        return msg

    def tombstone(self, *, channel_id: str, message_id: int, version_ts: datetime) -> Message | None:
        msg = self.session.scalar(
            select(Message).where(Message.channel_id == channel_id).where(Message.message_id == message_id)
        )
        if msg is None:
            return None
        if version_ts >= msg.latest_version_ts:
            msg.deleted = True
            msg.latest_version_ts = version_ts
            self.session.add(msg)
            self.session.flush()
        return msg

    def search_text(
        self,
        *,
        channel_id: str,
        query_terms: list[str],
        limit: int,
        include_quarantined: bool = False,
    ) -> list[Message]:
        # Simple MVP: fetch recent messages for channel and filter in python.
        stmt = (
            select(Message)
            .where(Message.channel_id == channel_id)
            .where(Message.deleted.is_(False))
            .order_by(Message.ts.desc())
            .limit(2000)
        )
        if not include_quarantined:
            stmt = stmt.where(Message.quarantined.is_(False))
        messages = list(self.session.scalars(stmt))

        def score(m: Message) -> int:
            t = (m.text or "").lower()
            return sum(1 for term in query_terms if term and term in t)

        scored = [(score(m), m) for m in messages]
        scored = [(s, m) for (s, m) in scored if s > 0]
        scored.sort(key=lambda x: (x[0], x[1].ts), reverse=True)
        return [m for _, m in scored[:limit]]

