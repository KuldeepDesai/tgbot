from __future__ import annotations

from datetime import datetime, timezone

from tgbot.ingestion.schema.event_envelope import EventEnvelope
from tgbot.lake.object_store.interface import ObjectStore
from tgbot.lake.reader import iter_events
from tgbot.logging.correlation import get_request_id
from tgbot.safety.message_classifier import classify_message
from tgbot.storage.repos.audit_repo import AuditRepo
from tgbot.storage.repos.messages_repo import MessagesRepo


def _extract_message_fields(env: EventEnvelope) -> tuple[datetime, str, dict, str | None]:
    """
    Extracts (ts_utc, text, raw_json, sender_id) from the raw Telegram update payload.
    Best-effort for MVP.
    """
    payload = env.payload or {}

    # Common Telegram shapes:
    # - {"update_id":..., "message": {...}}
    # - {"update_id":..., "edited_message": {...}}
    msg = payload.get("message") or payload.get("edited_message") or payload.get("channel_post") or payload
    text = msg.get("text") or msg.get("caption") or ""

    # Telegram "date"/"edit_date" are unix seconds.
    ts_sec = msg.get("date") or msg.get("edit_date")
    ts = datetime.fromtimestamp(ts_sec, tz=timezone.utc) if ts_sec else env.received_at

    sender = msg.get("from") or {}
    sender_id = str(sender.get("id")) if sender.get("id") is not None else None

    return ts, text, payload, sender_id


def process_lake_jsonl(
    *,
    store: ObjectStore,
    jsonl_path: str,
    messages_repo: MessagesRepo,
    audit_repo: AuditRepo,
) -> None:
    """
    Story 2.3: process window file into latest message state with edits and tombstones.
    """
    for env in iter_events(store, jsonl_path):
        if not env.channel_id:
            continue

        if env.event_type in ("message_new", "message_edit"):
            ts, text, raw_json, sender_id = _extract_message_fields(env)
            version_ts = env.received_at
            ms = classify_message(text)
            messages_repo.upsert_latest(
                channel_id=env.channel_id,
                message_id=env.message_id or 0,
                ts=ts,
                text=text,
                raw_json=raw_json,
                version_ts=version_ts,
                sender_id=sender_id,
                quarantined=ms.quarantined,
                quarantine_reason=ms.reason,
            )
        elif env.event_type == "message_delete":
            messages_repo.tombstone(
                channel_id=env.channel_id, message_id=env.message_id or 0, version_ts=env.received_at
            )
        else:
            # Non-message events are ignored by this worker stage (handled elsewhere).
            pass

    audit_repo.write(
        event_type="worker.file_processed",
        correlation_id=get_request_id(),
        channel_id=None,
        payload_json={"jsonl_path": jsonl_path},
    )

