from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class SafetyDecision:
    allowed: bool
    reason: str | None = None
    refusal_message: str | None = None


_FLAG_PATTERNS = [
    re.compile(r"\bkill myself\b", re.I),
    re.compile(r"\bsuicide\b", re.I),
    re.compile(r"\bbuy (a )?gun\b", re.I),
    re.compile(r"\bhow to make (a )?bomb\b", re.I),
]


def classify_query(query_text: str) -> SafetyDecision:
    qt = query_text or ""
    for pat in _FLAG_PATTERNS:
        if pat.search(qt):
            return SafetyDecision(
                allowed=False,
                reason="policy_flagged",
                refusal_message=(
                    "I can’t help with that. If you’re in immediate danger or feeling at risk, "
                    "please seek help from local emergency services or someone you trust."
                ),
            )
    return SafetyDecision(allowed=True)

