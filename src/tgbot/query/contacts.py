from __future__ import annotations

import re

_PHONE_RE = re.compile(r"(?<!\d)(?:\+91[-\s]?)?[6-9]\d{9}(?!\d)")


def extract_contacts(text: str) -> list[str]:
    if not text:
        return []
    phones = _PHONE_RE.findall(text)
    # De-dupe preserving order
    seen: set[str] = set()
    out: list[str] = []
    for p in phones:
        p = p.strip()
        if p and p not in seen:
            seen.add(p)
            out.append(p)
    return out

