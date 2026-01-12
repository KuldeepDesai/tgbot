from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class MessageSafety:
    quarantined: bool
    reason: str | None = None


_QUARANTINE_PATTERNS = [
    re.compile(r"\b(buy|sell)\b.*\b(drugs|cocaine|heroin)\b", re.I),
    re.compile(r"\bchild porn\b", re.I),
]


def classify_message(text: str) -> MessageSafety:
    t = text or ""
    for pat in _QUARANTINE_PATTERNS:
        if pat.search(t):
            return MessageSafety(quarantined=True, reason="policy_quarantine")
    return MessageSafety(quarantined=False, reason=None)

