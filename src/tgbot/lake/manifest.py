from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass(frozen=True)
class LakeManifest:
    schema_version: int
    channel_id: str
    window_start: datetime
    window_end: datetime
    counts_by_event_type: dict[str, int]
    content_etag: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "channel_id": self.channel_id,
            "window_start": self.window_start.isoformat(),
            "window_end": self.window_end.isoformat(),
            "counts_by_event_type": self.counts_by_event_type,
            "content_etag": self.content_etag,
        }

    @staticmethod
    def from_events(
        *, schema_version: int, channel_id: str, window_start: datetime, window_end: datetime, event_types: list[str], content_etag: str
    ) -> "LakeManifest":
        return LakeManifest(
            schema_version=schema_version,
            channel_id=channel_id,
            window_start=window_start,
            window_end=window_end,
            counts_by_event_type=dict(Counter(event_types)),
            content_etag=content_etag,
        )

