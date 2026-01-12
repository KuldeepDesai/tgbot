from __future__ import annotations

import json
from datetime import datetime, timezone
import uuid

from tgbot.ingestion.queue.interface import Queue
from tgbot.ingestion.schema.event_envelope import EventEnvelope
from tgbot.logging.correlation import get_request_id
from tgbot.storage.repos.audit_repo import AuditRepo
from tgbot.storage.repos.cursors_repo import CursorsRepo
from tgbot.storage.repos.channels_repo import ChannelsRepo
from tgbot.userbot.telethon_client import make_telethon_client


async def backfill_channel(
    *,
    telegram_chat_id: str,
    queue: Queue,
    channels_repo: ChannelsRepo,
    cursors_repo: CursorsRepo,
    audit_repo: AuditRepo,
    page_size: int = 200,
) -> int:
    """
    Story 2.4: fetch history via Client API, enqueue envelopes with source=userbot, persist cursor.
    Returns count enqueued.
    """
    ch = channels_repo.get_by_telegram_chat_id(telegram_chat_id)
    if ch is None:
        raise ValueError("channel not registered")

    cur = cursors_repo.get(ch.id)
    min_id = cur.last_seen_message_id if cur and cur.last_seen_message_id else 0

    client = make_telethon_client()
    enqueued = 0

    async with client:
        # Telethon iter_messages newest->oldest by default; we want messages newer than cursor.
        # We'll fetch in ascending order by collecting then reversing.
        batch = []
        async for msg in client.iter_messages(int(telegram_chat_id), min_id=min_id, limit=page_size):
            batch.append(msg)
        batch.reverse()

        for msg in batch:
            payload = {"userbot_message": msg.to_dict()}
            namespace = uuid.UUID("00000000-0000-0000-0000-000000000002")
            event_id = str(uuid.uuid5(namespace, f"userbot:{telegram_chat_id}:{msg.id}"))
            env = EventEnvelope(
                event_id=event_id,
                source="userbot",
                telegram_chat_id=telegram_chat_id,
                channel_id=ch.id,
                event_type="message_new",
                message_id=msg.id,
                payload=payload,
            )
            queue.enqueue(json.dumps(env.model_dump(mode="json"), ensure_ascii=False))
            enqueued += 1
            min_id = max(min_id, int(msg.id))

        # Persist cursor after batch
        cursors_repo.upsert(
            channel_id=ch.id,
            last_seen_message_id=min_id if min_id else None,
            last_seen_ts=datetime.now(timezone.utc),
        )
        audit_repo.write(
            event_type="backfill.cursor_advanced",
            correlation_id=get_request_id(),
            channel_id=ch.id,
            payload_json={"telegram_chat_id": telegram_chat_id, "last_seen_message_id": min_id, "enqueued": enqueued},
        )

    return enqueued

