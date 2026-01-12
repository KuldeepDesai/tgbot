from __future__ import annotations


def more_recs_keyboard(*, answer_id: str, offset: int, has_more: bool):
    """
    Returns aiogram InlineKeyboardMarkup (or None if aiogram isn't available).
    """
    if not has_more:
        return None
    try:
        from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
    except Exception:  # pragma: no cover
        return None

    rows = []
    if has_more:
        data = f"more_recs:{answer_id}:{offset}"
        rows.append([InlineKeyboardButton(text="More recommendations", callback_data=data)])
    # Feedback buttons (Story 5.3) - also works as fallback if reactions aren't delivered.
    rows.append(
        [
            InlineKeyboardButton(text="👍", callback_data=f"feedback:{answer_id}:up"),
            InlineKeyboardButton(text="👎", callback_data=f"feedback:{answer_id}:down"),
        ]
    )
    return InlineKeyboardMarkup(inline_keyboard=rows)

