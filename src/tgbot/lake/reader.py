from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Iterator

from tgbot.ingestion.schema.event_envelope import EventEnvelope
from tgbot.lake.object_store.interface import ObjectStore


@dataclass(frozen=True)
class LakeFile:
    jsonl_path: str
    manifest_path: str


def iter_events(store: ObjectStore, jsonl_path: str) -> Iterator[EventEnvelope]:
    data = store.get_bytes(jsonl_path).decode("utf-8")
    for line in data.splitlines():
        if not line.strip():
            continue
        yield EventEnvelope.model_validate(json.loads(line))

