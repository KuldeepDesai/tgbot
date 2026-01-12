from __future__ import annotations

from tgbot.telegram.handlers.query import build_more_recs_page
from tgbot.telegram.ui.keyboards import more_recs_keyboard


def parse_callback_data(data: str) -> tuple[str, int] | None:
    # more_recs:<answer_id>:<offset>
    if not data or not data.startswith("more_recs:"):
        return None
    parts = data.split(":")
    if len(parts) != 3:
        return None
    answer_id = parts[1]
    try:
        offset = int(parts[2])
    except Exception:
        return None
    return answer_id, offset


def handle_more_recs(*, callback_data: str):
    parsed = parse_callback_data(callback_data)
    if not parsed:
        return None
    answer_id, offset = parsed
    text, has_more, shown = build_more_recs_page(answer_id=answer_id, offset=offset)
    kb = more_recs_keyboard(answer_id=answer_id, offset=offset + shown, has_more=has_more)
    return text, kb

