from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime

from tgbot.query.contacts import extract_contacts
from tgbot.storage.models.messages import Message


@dataclass(frozen=True)
class Citation:
    message_id: int
    message_ts: datetime
    text: str
    url: str | None = None


@dataclass(frozen=True)
class Recommendation:
    provider_key: str
    title: str
    contacts: list[str]
    citations: list[Citation]
    stance: str  # positive|negative|mixed|unknown


_PROVIDER_HINT_RE = re.compile(r"^(?P<name>[A-Za-z][\w\s.&'-]{2,48})(?:\s*[-:]\s*|\s+is\s+)", re.I)
_NEG_RE = re.compile(r"\b(avoid|scam|fraud|bad|worst|don'?t)\b", re.I)
_POS_RE = re.compile(r"\b(recommend|good|great|best|trusted|reliable)\b", re.I)


def provider_key_from_text(text: str) -> str:
    t = (text or "").strip()
    m = _PROVIDER_HINT_RE.match(t)
    if m:
        name = m.group("name").strip()
        return re.sub(r"\s+", " ", name).lower()
    # fallback: first ~6 words as a key
    words = re.findall(r"[A-Za-z0-9]+", t)[:6]
    return " ".join(words).lower() if words else "unknown"


def stance_from_text(text: str) -> str:
    t = text or ""
    neg = bool(_NEG_RE.search(t))
    pos = bool(_POS_RE.search(t))
    if pos and neg:
        return "mixed"
    if pos:
        return "positive"
    if neg:
        return "negative"
    return "unknown"


def build_recommendations(messages: list[Message], *, max_distinct: int) -> list[Recommendation]:
    by_key: dict[str, list[Message]] = {}
    for m in messages:
        key = provider_key_from_text(m.text)
        by_key.setdefault(key, []).append(m)

    # rank providers by (best stance, recency, evidence count)
    def provider_score(msgs: list[Message]) -> tuple[int, datetime, int]:
        stances = [stance_from_text(mm.text) for mm in msgs]
        # Prefer positive over unknown over mixed over negative for MVP default.
        best = 0
        if "positive" in stances:
            best = 3
        elif "unknown" in stances:
            best = 2
        elif "mixed" in stances:
            best = 1
        else:
            best = 0
        newest = max(mm.ts for mm in msgs)
        return best, newest, len(msgs)

    items = sorted(by_key.items(), key=lambda kv: provider_score(kv[1]), reverse=True)
    out: list[Recommendation] = []
    for key, msgs in items:
        if len(out) >= max_distinct:
            break
        msgs = sorted(msgs, key=lambda m: m.ts, reverse=True)[:3]
        contacts: list[str] = []
        for mm in msgs:
            contacts.extend(extract_contacts(mm.text))
        # de-dupe contacts
        contacts = list(dict.fromkeys(contacts))
        stance = "mixed" if any(stance_from_text(mm.text) == "negative" for mm in msgs) and any(
            stance_from_text(mm.text) == "positive" for mm in msgs
        ) else stance_from_text(msgs[0].text)
        citations = [
            Citation(message_id=mm.message_id, message_ts=mm.ts, text=(mm.text or "")[:200], url=None)
            for mm in msgs
        ]
        title = msgs[0].text.splitlines()[0][:80] if msgs[0].text else key
        out.append(Recommendation(provider_key=key, title=title, contacts=contacts, citations=citations, stance=stance))
    return out

