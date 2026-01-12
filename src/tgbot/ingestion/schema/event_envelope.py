from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any, Literal

from pydantic import BaseModel, Field

EventSource = Literal["bot_api", "userbot"]
EventType = Literal[
    "message_new",
    "message_edit",
    "message_delete",
    "reaction_update",
    "bot_membership_update",
]


class EventEnvelope(BaseModel):
    """
    Durable ingest contract. JSON keys are snake_case.
    """

    event_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    received_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    source: EventSource
    schema_version: int = 1

    telegram_chat_id: str
    channel_id: str | None = None

    event_type: EventType
    message_id: int | None = None

    payload: dict[str, Any]

