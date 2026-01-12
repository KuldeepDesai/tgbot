from __future__ import annotations

import json

from tgbot.config.settings import get_settings
from tgbot.ingestion.queue.factory import get_queue
from tgbot.logging.correlation import get_request_id, request_id_scope
from tgbot.logging.logger import get_logger
from tgbot.storage.db import db_session
from tgbot.storage.repos.audit_repo import AuditRepo
from tgbot.storage.repos.channels_repo import ChannelsRepo
from tgbot.telegram.updates.normalization import normalize_update, to_envelope

logger = get_logger(__name__, service="receiver")


async def run_polling() -> None:
    settings = get_settings()
    if not settings.telegram_bot_token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is required")

    try:
        from aiogram import Bot, Dispatcher
        from aiogram.enums import ParseMode
        from aiogram.types import CallbackQuery, Message, Update
    except Exception as e:  # pragma: no cover
        raise RuntimeError("aiogram is required to run receiver") from e

    bot = Bot(settings.telegram_bot_token, parse_mode=ParseMode.MARKDOWN_V2)
    dp = Dispatcher()

    queue = get_queue()

    @dp.update()
    async def on_update(update: Update) -> None:
        with request_id_scope():
            raw = update.model_dump()
            nu = normalize_update(raw)
            if nu is None:
                return

            with db_session() as s:
                channels = ChannelsRepo(s)
                audit = AuditRepo(s)

                ch = channels.get_by_telegram_chat_id(nu.telegram_chat_id)
                if ch is None:
                    audit.write(
                        event_type="ingest.unknown_channel",
                        correlation_id=get_request_id(),
                        channel_id=None,
                        payload_json={"telegram_chat_id": nu.telegram_chat_id, "event_type": nu.event_type},
                    )
                    return

                if not ch.ingestion_enabled:
                    return

                env = to_envelope(normalized=nu, source="bot_api", channel_id=ch.id)
                queue.enqueue(json.dumps(env.model_dump(mode="json"), ensure_ascii=False))
                audit.write(
                    event_type="ingest.enqueued",
                    correlation_id=get_request_id(),
                    channel_id=ch.id,
                    payload_json={"event_id": env.event_id, "event_type": env.event_type},
                )

                # Bot membership change detection (Story 6.1)
                if nu.event_type == "bot_membership_update":
                    new_status = (
                        raw.get("my_chat_member", {}).get("new_chat_member", {}).get("status")
                        if isinstance(raw.get("my_chat_member"), dict)
                        else None
                    )
                    if new_status in ("kicked", "left"):
                        channels.set_ingestion_enabled(ch.id, False)
                        audit.write(
                            event_type="bot.removed",
                            correlation_id=get_request_id(),
                            channel_id=ch.id,
                            payload_json={"telegram_chat_id": nu.telegram_chat_id, "new_status": new_status},
                        )
                    elif new_status and new_status != "member":
                        # Best-effort: record and degrade ingestion to avoid noisy loops if permissions are reduced.
                        channels.set_ingestion_enabled(ch.id, False)
                        audit.write(
                            event_type="bot.permissions_changed",
                            correlation_id=get_request_id(),
                            channel_id=ch.id,
                            payload_json={"telegram_chat_id": nu.telegram_chat_id, "new_status": new_status},
                        )

                # Feedback capture from reactions (Story 5.3), if Telegram exposes it.
                if nu.event_type == "reaction_update" and nu.message_id:
                    try:
                        from tgbot.storage.repos.answers_repo import AnswersRepo

                        reaction = (
                            raw.get("message_reaction", {}).get("new_reaction", [])
                            if isinstance(raw.get("message_reaction"), dict)
                            else []
                        )
                        emojis = []
                        for r in reaction:
                            emoji = (r.get("emoji") if isinstance(r, dict) else None) or (
                                r.get("type", {}).get("emoji") if isinstance(r, dict) and isinstance(r.get("type"), dict) else None
                            )
                            if emoji:
                                emojis.append(emoji)
                        kind = "up" if "👍" in emojis else "down" if "👎" in emojis else None
                        if kind:
                            ans = AnswersRepo(s).get_by_telegram_message_id(int(nu.message_id))
                            audit.write(
                                event_type="feedback.captured",
                                correlation_id=get_request_id(),
                                channel_id=ans.channel_id if ans else ch.id,
                                payload_json={
                                    "kind": kind,
                                    "telegram_message_id": nu.message_id,
                                    "answer_id": ans.id if ans else None,
                                },
                            )
                    except Exception:
                        pass

    # /help handler (Story 1.3)
    @dp.message(lambda m: m.text and m.text.startswith("/help"))
    async def help_handler(message: Message) -> None:
        from tgbot.telegram.handlers.help import build_help_text

        with request_id_scope():
            text = build_help_text(telegram_chat_id=str(message.chat.id))
            await message.answer(text, reply_to_message_id=message.message_id)

    # Question handler (Stories 3.1, 3.2, 3.4, 4.1, 5.1)
    @dp.message(lambda m: bool(m.text))
    async def message_handler(message: Message) -> None:
        from aiogram.enums import ChatAction
        from tgbot.telegram.handlers.query import FAIL_FALLBACK_TEXT, build_answer_for_message, is_question_text

        with request_id_scope():
            bot_user = await bot.me()
            bot_username = bot_user.username
            is_reply_to_bot = bool(message.reply_to_message and message.reply_to_message.from_user and message.reply_to_message.from_user.id == bot_user.id)

            if not is_question_text(text=message.text or "", bot_username=bot_username, is_reply_to_bot=is_reply_to_bot):
                return

            # typing immediately (Story 3.2)
            await bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.TYPING)

            try:
                text, answer_id, shown = build_answer_for_message(
                    telegram_chat_id=str(message.chat.id),
                    query_text=message.text or "",
                    consume_quota=True,
                )
                kb = None
                if answer_id:
                    kb = more_recs_keyboard(answer_id=answer_id, offset=shown, has_more=True)
                sent = await message.answer(text, reply_to_message_id=message.message_id, reply_markup=kb)
                # best-effort: store telegram_message_id for feedback linking
                if answer_id:
                    from tgbot.storage.repos.answers_repo import AnswersRepo

                    with db_session() as s:
                        AnswersRepo(s).set_telegram_message_id(answer_id, sent.message_id)
            except Exception:
                await message.answer(FAIL_FALLBACK_TEXT, reply_to_message_id=message.message_id)

    # More recommendations callback (Story 4.2)
    @dp.callback_query(lambda c: c.data and c.data.startswith("more_recs:"))
    async def more_recs_handler(callback: CallbackQuery) -> None:
        from tgbot.telegram.handlers.callbacks_more_recs import handle_more_recs

        with request_id_scope():
            res = handle_more_recs(callback_data=callback.data or "")
            if res is None:
                await callback.answer()
                return
            text, kb = res
            if callback.message:
                await callback.message.answer(text, reply_to_message_id=callback.message.message_id, reply_markup=kb)
            await callback.answer()

    # Feedback callback fallback (Story 5.3)
    @dp.callback_query(lambda c: c.data and c.data.startswith("feedback:"))
    async def feedback_handler(callback: CallbackQuery) -> None:
        from tgbot.telegram.handlers.feedback import parse_feedback_callback, record_feedback_event

        with request_id_scope():
            parsed = parse_feedback_callback(callback.data or "")
            if not parsed:
                await callback.answer()
                return
            answer_id, kind = parsed
            user_id = str(callback.from_user.id) if callback.from_user else None
            telegram_message_id = callback.message.message_id if callback.message else None
            record_feedback_event(
                answer_id=answer_id, kind=kind, user_id=user_id, telegram_message_id=telegram_message_id
            )
            await callback.answer("Thanks!")

    logger.info("receiver.polling.start", extra={"request_id": get_request_id()})
    await dp.start_polling(bot)

