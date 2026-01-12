from __future__ import annotations

import argparse
import asyncio
from datetime import datetime, timezone

from tgbot.config.settings import get_settings
from tgbot.logging.correlation import get_request_id, request_id_scope
from tgbot.logging.logger import get_logger
from tgbot.storage.db import db_session
from tgbot.storage.repos.audit_repo import AuditRepo
from tgbot.storage.repos.channels_repo import ChannelsRepo
from tgbot.ingestion.queue.factory import get_queue
from tgbot.storage.repos.cursors_repo import CursorsRepo

logger = get_logger(__name__, service="cli")


def _validate_telegram_chat_id(raw: str) -> str:
    raw = (raw or "").strip()
    if not raw or not raw.lstrip("-").isdigit():
        raise ValueError("telegram_chat_id must be an integer-like string")
    return raw


def _validate_disclaimer(text: str) -> str:
    t = (text or "").strip()
    if not t:
        raise ValueError("disclaimer_text must be non-empty")
    return t


async def _send_message(telegram_chat_id: str, text: str) -> None:
    settings = get_settings()
    if not settings.telegram_bot_token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is required")
    from aiogram import Bot

    bot = Bot(settings.telegram_bot_token)
    await bot.send_message(chat_id=int(telegram_chat_id), text=text)


def cmd_register_channel(args: argparse.Namespace) -> int:
    telegram_chat_id = _validate_telegram_chat_id(args.telegram_chat_id)
    disclaimer_text = _validate_disclaimer(args.disclaimer_text)

    with request_id_scope():
        with db_session() as s:
            channels = ChannelsRepo(s)
            audit = AuditRepo(s)

            res = channels.upsert_channel(telegram_chat_id=telegram_chat_id, disclaimer_text=disclaimer_text)

            logger.info(
                "channel.upsert",
                extra={
                    "request_id": get_request_id(),
                    "channel_id": res.channel.id,
                    "telegram_chat_id": telegram_chat_id,
                    "action": res.action,
                },
            )
            audit.write(
                event_type="channel.upsert",
                correlation_id=get_request_id(),
                channel_id=res.channel.id,
                payload_json={"telegram_chat_id": telegram_chat_id, "action": res.action},
                event_ts=datetime.now(timezone.utc),
            )

            print(
                {
                    "ok": True,
                    "channel_id": res.channel.id,
                    "telegram_chat_id": res.channel.telegram_chat_id,
                    "action": res.action,
                    "note": "Changes are effective after app restart (MVP).",
                }
            )
    return 0


def cmd_send(args: argparse.Namespace) -> int:
    telegram_chat_id = _validate_telegram_chat_id(args.telegram_chat_id)
    text = (args.text or "").strip()
    if not text:
        raise ValueError("--text is required")

    with request_id_scope():
        asyncio.run(_send_message(telegram_chat_id, text))
        with db_session() as s:
            channels = ChannelsRepo(s)
            audit = AuditRepo(s)
            ch = channels.get_by_telegram_chat_id(telegram_chat_id)
            audit.write(
                event_type="ops.send",
                correlation_id=get_request_id(),
                channel_id=ch.id if ch else None,
                payload_json={"telegram_chat_id": telegram_chat_id, "text": text},
            )
    return 0


def cmd_broadcast(args: argparse.Namespace) -> int:
    text = (args.text or "").strip()
    if not text:
        raise ValueError("--text is required")

    with request_id_scope():
        with db_session() as s:
            channels = ChannelsRepo(s)
            audit = AuditRepo(s)
            all_channels = channels.list_all()

        async def _run():
            for ch in all_channels:
                try:
                    await _send_message(ch.telegram_chat_id, text)
                    with db_session() as s2:
                        AuditRepo(s2).write(
                            event_type="ops.broadcast.send",
                            correlation_id=get_request_id(),
                            channel_id=ch.id,
                            payload_json={"telegram_chat_id": ch.telegram_chat_id, "text": text},
                        )
                except Exception as e:
                    with db_session() as s2:
                        AuditRepo(s2).write(
                            event_type="ops.broadcast.error",
                            correlation_id=get_request_id(),
                            channel_id=ch.id,
                            payload_json={"telegram_chat_id": ch.telegram_chat_id, "error": str(e)},
                        )

        asyncio.run(_run())
    return 0


def cmd_backfill(args: argparse.Namespace) -> int:
    telegram_chat_id = _validate_telegram_chat_id(args.telegram_chat_id)
    page_size = int(args.page_size)
    if page_size <= 0:
        raise ValueError("--page-size must be > 0")

    from tgbot.userbot.backfill import backfill_channel

    with request_id_scope():
        q = get_queue()
        with db_session() as s:
            channels = ChannelsRepo(s)
            cursors = CursorsRepo(s)
            audit = AuditRepo(s)
            count = asyncio.run(
                backfill_channel(
                    telegram_chat_id=telegram_chat_id,
                    queue=q,
                    channels_repo=channels,
                    cursors_repo=cursors,
                    audit_repo=audit,
                    page_size=page_size,
                )
            )
            print({"ok": True, "telegram_chat_id": telegram_chat_id, "enqueued": count})
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="tgbot-ops")
    sub = p.add_subparsers(dest="cmd", required=True)

    reg = sub.add_parser("register-channel", help="Upsert a channel and disclaimer")
    reg.add_argument("--telegram-chat-id", required=True)
    reg.add_argument("--disclaimer-text", required=True)
    reg.set_defaults(func=cmd_register_channel)

    send = sub.add_parser("send", help="Send an ops message to one channel")
    send.add_argument("--telegram-chat-id", required=True)
    send.add_argument("--text", required=True)
    send.set_defaults(func=cmd_send)

    bc = sub.add_parser("broadcast", help="Broadcast an ops message to all channels")
    bc.add_argument("--text", required=True)
    bc.set_defaults(func=cmd_broadcast)

    bf = sub.add_parser("backfill", help="Backfill historical messages via userbot (Telethon)")
    bf.add_argument("--telegram-chat-id", required=True)
    bf.add_argument("--page-size", type=int, default=200)
    bf.set_defaults(func=cmd_backfill)

    return p


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())

