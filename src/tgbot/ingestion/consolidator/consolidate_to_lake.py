from __future__ import annotations

import json
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

from tgbot.ingestion.queue.interface import Queue
from tgbot.ingestion.schema.event_envelope import EventEnvelope
from tgbot.lake.manifest import LakeManifest
from tgbot.lake.object_store.interface import ObjectStore
from tgbot.lake.paths import window_paths
from tgbot.logging.correlation import get_request_id
from tgbot.storage.repos.audit_repo import AuditRepo


WINDOW_HOURS = 4


@dataclass(frozen=True)
class ConsolidationResult:
    written_files: int
    skipped_existing: int


def _floor_to_window_start(ts: datetime) -> datetime:
    ts = ts.astimezone(timezone.utc)
    hour = (ts.hour // WINDOW_HOURS) * WINDOW_HOURS
    return ts.replace(minute=0, second=0, microsecond=0, hour=hour)


def _window_end(start: datetime) -> datetime:
    return start + timedelta(hours=WINDOW_HOURS)


def consolidate_once(
    *,
    queue: Queue,
    store: ObjectStore,
    audit: AuditRepo,
    max_messages: int = 512,
) -> ConsolidationResult:
    msgs = queue.dequeue_batch(max_messages=max_messages)
    envelopes: list[EventEnvelope] = []
    for m in msgs:
        try:
            envelopes.append(EventEnvelope.model_validate(json.loads(m.body)))
        except Exception:
            # drop bad message; not ideal but avoids poison pills in MVP
            queue.delete(m.message_id)

    buckets: dict[tuple[str, datetime], list[EventEnvelope]] = defaultdict(list)
    for env in envelopes:
        if not env.channel_id:
            continue
        ws = _floor_to_window_start(env.received_at)
        buckets[(env.channel_id, ws)].append(env)

    written = 0
    skipped = 0

    for (channel_id, ws), envs in buckets.items():
        we = _window_end(ws)
        p = window_paths(channel_id=channel_id, window_start=ws, window_end=we)

        if store.exists(p.jsonl_path) or store.exists(p.manifest_path):
            skipped += 1
            audit.write(
                event_type="lake.window.exists",
                correlation_id=get_request_id(),
                channel_id=channel_id,
                payload_json={"jsonl_path": p.jsonl_path, "manifest_path": p.manifest_path},
            )
            continue

        jsonl_lines = [json.dumps(env.model_dump(mode="json"), ensure_ascii=False) for env in envs]
        jsonl_bytes = ("\n".join(jsonl_lines) + "\n").encode("utf-8")
        etag = store.put_bytes(p.jsonl_path, jsonl_bytes)

        manifest = LakeManifest.from_events(
            schema_version=1,
            channel_id=channel_id,
            window_start=ws,
            window_end=we,
            event_types=[e.event_type for e in envs],
            content_etag=etag,
        )
        store.put_bytes(p.manifest_path, json.dumps(manifest.to_dict(), ensure_ascii=False).encode("utf-8"))

        audit.write(
            event_type="lake.written",
            correlation_id=get_request_id(),
            channel_id=channel_id,
            payload_json={"jsonl_path": p.jsonl_path, "manifest_path": p.manifest_path, "etag": etag},
        )
        written += 1

    # ack queue messages after successful consolidation attempt (best-effort)
    for m in msgs:
        queue.delete(m.message_id)

    return ConsolidationResult(written_files=written, skipped_existing=skipped)

