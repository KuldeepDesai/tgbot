from __future__ import annotations

import re

# Telegram MarkdownV2 reserved characters:
# _ * [ ] ( ) ~ ` > # + - = | { } . !
_MDV2_RE = re.compile(r"([_*\[\]()~`>#+\-=|{}.!])")


def escape_markdown_v2(text: str) -> str:
    """
    Escape dynamic text so Telegram MarkdownV2 rendering is safe.

    IMPORTANT: Use this for any user-/message-/db-derived text that will be sent with parse_mode=MarkdownV2.
    """
    if text is None:
        return ""
    return _MDV2_RE.sub(r"\\\1", str(text))

