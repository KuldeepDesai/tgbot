from __future__ import annotations

from tgbot.storage.db import db_session
from tgbot.storage.repos.channels_repo import ChannelsRepo
from tgbot.telegram.markdown_v2 import escape_markdown_v2


HELP_USAGE = (
    "To ask a question:\n"
    "- Mention the bot in a message (e.g. @YourBot what’s a good electrician?)\n"
    "- Or reply to a bot answer in a thread with a follow-up question.\n"
)


def build_help_text(*, telegram_chat_id: str) -> str:
    with db_session() as s:
        repo = ChannelsRepo(s)
        ch = repo.get_by_telegram_chat_id(telegram_chat_id)

    if ch is None:
        return escape_markdown_v2("This channel is not configured for the bot yet.")

    disclaimer = escape_markdown_v2(ch.disclaimer_text)
    return (
        f"*{escape_markdown_v2('How to use this bot')}*\n\n"
        f"{escape_markdown_v2(HELP_USAGE)}\n"
        f"*{escape_markdown_v2('Disclaimer')}*\n"
        f"{disclaimer}"
    )

