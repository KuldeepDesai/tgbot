from __future__ import annotations

from tgbot.config.settings import get_settings


def make_telethon_client():
    settings = get_settings()
    if not settings.telethon_api_id or not settings.telethon_api_hash or not settings.telethon_session:
        raise RuntimeError("Telethon credentials are required: TELETHON_API_ID/TELETHON_API_HASH/TELETHON_SESSION")
    from telethon import TelegramClient

    return TelegramClient(settings.telethon_session, settings.telethon_api_id, settings.telethon_api_hash)

