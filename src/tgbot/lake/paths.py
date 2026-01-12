from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class LakeWindowPaths:
    jsonl_path: str
    manifest_path: str


def window_paths(*, channel_id: str, window_start: datetime, window_end: datetime) -> LakeWindowPaths:
    # Deterministic path; always UTC.
    y = window_start.strftime("%Y")
    m = window_start.strftime("%m")
    d = window_start.strftime("%d")
    h = window_start.strftime("%H00")
    h2 = window_end.strftime("%H00")
    base = f"raw/channel/{channel_id}/{y}/{m}/{d}/{h}-{h2}"
    return LakeWindowPaths(jsonl_path=f"{base}.jsonl", manifest_path=f"{base}.manifest.json")

