from __future__ import annotations

from dataclasses import dataclass
import uuid
from typing import Any

from tgbot.ingestion.schema.event_envelope import EventEnvelope, EventType


@dataclass(frozen=True)
class NormalizedUpdate:
    telegram_chat_id: str
    message_id: int | None
    event_type: EventType
    payload: dict[str, Any]
    idempotency_key: str


def normalize_update(update_dict: dict[str, Any]) -> NormalizedUpdate | None:
    """
    Best-effort normalization from raw Telegram update JSON (as dict).
    """
    update_id = update_dict.get("update_id")
    if "message" in update_dict:
        msg = update_dict["message"] or {}
        chat = msg.get("chat") or {}
        idem = f"{chat.get('id')}:{update_id}:message_new:{msg.get('message_id')}"
        return NormalizedUpdate(
            telegram_chat_id=str(chat.get("id")),
            message_id=msg.get("message_id"),
            event_type="message_new",
            payload=update_dict,
            idempotency_key=idem,
        )
    if "edited_message" in update_dict:
        msg = update_dict["edited_message"] or {}
        chat = msg.get("chat") or {}
        idem = f"{chat.get('id')}:{update_id}:message_edit:{msg.get('message_id')}"
        return NormalizedUpdate(
            telegram_chat_id=str(chat.get("id")),
            message_id=msg.get("message_id"),
            event_type="message_edit",
            payload=update_dict,
            idempotency_key=idem,
        )
    if "my_chat_member" in update_dict:
        mcm = update_dict["my_chat_member"] or {}
        chat = mcm.get("chat") or {}
        idem = f"{chat.get('id')}:{update_id}:bot_membership_update"
        return NormalizedUpdate(
            telegram_chat_id=str(chat.get("id")),
            message_id=None,
            event_type="bot_membership_update",
            payload=update_dict,
            idempotency_key=idem,
        )
    if "message_reaction" in update_dict:
        mr = update_dict["message_reaction"] or {}
        chat = mr.get("chat") or {}
        idem = f"{chat.get('id')}:{update_id}:reaction_update:{mr.get('message_id')}"
        return NormalizedUpdate(
            telegram_chat_id=str(chat.get("id")),
            message_id=mr.get("message_id"),
            event_type="reaction_update",
            payload=update_dict,
            idempotency_key=idem,
        )
    # Deletions are not reliably exposed to bots; reserved event type.
    return None


def to_envelope(*, normalized: NormalizedUpdate, source: str, channel_id: str | None) -> EventEnvelope:
    # Deterministic event_id so enqueue retries are safe.
    namespace = uuid.UUID("00000000-0000-0000-0000-000000000001")
    event_id = str(uuid.uuid5(namespace, f"{source}:{normalized.idempotency_key}"))
    return EventEnvelope(
        event_id=event_id,
        source=source,  # type: ignore[arg-type]
        telegram_chat_id=normalized.telegram_chat_id,
        channel_id=channel_id,
        event_type=normalized.event_type,
        message_id=normalized.message_id,
        payload=normalized.payload,
    )

