from __future__ import annotations

from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from tgbot.storage.models.audit_events import AuditEvent
from tgbot.storage.db import utc_now


class AuditRepo:
    def __init__(self, session: Session):
        self.session = session

    def write(
        self,
        *,
        event_type: str,
        correlation_id: str,
        channel_id: str | None = None,
        payload_json: dict | None = None,
        event_ts: datetime | None = None,
    ) -> AuditEvent:
        ev = AuditEvent(
            event_type=event_type,
            event_ts=event_ts or utc_now(),
            channel_id=channel_id,
            correlation_id=correlation_id,
            payload_json=payload_json or {},
        )
        self.session.add(ev)
        self.session.flush()
        return ev

    def list_by_type_and_range(
        self, *, event_type: str, start_ts: datetime, end_ts: datetime
    ) -> list[AuditEvent]:
        stmt = (
            select(AuditEvent)
            .where(AuditEvent.event_type == event_type)
            .where(AuditEvent.event_ts >= start_ts)
            .where(AuditEvent.event_ts <= end_ts)
            .order_by(AuditEvent.event_ts.asc())
        )
        return list(self.session.scalars(stmt))

