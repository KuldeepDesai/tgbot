from __future__ import annotations

from datetime import datetime, timezone

from tgbot.logging.correlation import get_request_id
from tgbot.safety.query_gate import classify_query
from tgbot.storage.db import db_session
from tgbot.storage.repos.answers_repo import AnswersRepo
from tgbot.storage.repos.audit_repo import AuditRepo
from tgbot.storage.repos.channels_repo import ChannelsRepo
from tgbot.storage.repos.messages_repo import MessagesRepo
from tgbot.storage.repos.quota_repo import QuotaRepo
from tgbot.telegram.ui.answer_format import format_answer_markdown_v2
from tgbot.telegram.ui.keyboards import more_recs_keyboard
from tgbot.query.service import answer_query


DAILY_QUOTA = 50
QUOTA_EXHAUSTED_TEXT = "Daily quota is over; try again after midnight IST."
FAIL_FALLBACK_TEXT = "Sorry, I couldn’t answer right now—please try again later."


def is_question_text(*, text: str, bot_username: str | None, is_reply_to_bot: bool) -> bool:
    if is_reply_to_bot:
        return True
    if bot_username and text and f"@{bot_username.lower()}" in text.lower():
        return True
    return False


def build_answer_for_message(
    *,
    telegram_chat_id: str,
    query_text: str,
    consume_quota: bool,
) -> tuple[str, str | None, int]:
    """
    Returns (markdown_text, answer_id, shown_count).
    """
    decision = classify_query(query_text)
    if not decision.allowed:
        return decision.refusal_message or "I can’t help with that.", None, 0

    with db_session() as s:
        channels = ChannelsRepo(s)
        audit = AuditRepo(s)
        quota = QuotaRepo(s)
        answers = AnswersRepo(s)
        messages = MessagesRepo(s)

        ch = channels.get_by_telegram_chat_id(telegram_chat_id)
        if ch is None:
            return "This channel is not configured for the bot yet.", None, 0

        now = datetime.now(timezone.utc)
        if consume_quota:
            allowed, _remaining = quota.try_consume_question(channel_id=ch.id, now_utc=now, daily_limit=DAILY_QUOTA)
            if not allowed:
                audit.write(
                    event_type="quota.exhausted",
                    correlation_id=get_request_id(),
                    channel_id=ch.id,
                    payload_json={"telegram_chat_id": telegram_chat_id},
                )
                return QUOTA_EXHAUSTED_TEXT, None, 0

        result = answer_query(channel_id=ch.id, query_text=query_text, messages_repo=messages, max_distinct=12)
        recs = result.recommendations
        show_disagreement = any(r.stance in ("mixed", "negative") for r in recs[:3]) and any(
            r.stance == "positive" for r in recs[:3]
        )

        # Cache full list for pagination/idempotency
        recommendations_json = [
            {
                "provider_key": r.provider_key,
                "title": r.title,
                "contacts": r.contacts,
                "stance": r.stance,
                "citations": [
                    {"message_id": c.message_id, "message_ts": c.message_ts.isoformat(), "url": c.url}
                    for c in r.citations
                ],
            }
            for r in recs
        ]
        ans = answers.create(
            channel_id=ch.id,
            query_text=query_text,
            cutoff_ts=result.cutoff_ts,
            recommendations_json=recommendations_json,
        )

        audit.write(
            event_type="answer.generated",
            correlation_id=get_request_id(),
            channel_id=ch.id,
            payload_json={"answer_id": ans.id},
        )

        top3 = recs[:3]
        text = format_answer_markdown_v2(
            query_text=query_text,
            cutoff_ts_utc=result.cutoff_ts,
            recommendations=top3,
            show_disagreement_note=show_disagreement,
        )
        return text, ans.id, len(top3)


def build_more_recs_page(*, answer_id: str, offset: int) -> tuple[str, bool, int]:
    """
    Returns (markdown_text, has_more, shown_count_this_page).
    """
    with db_session() as s:
        answers = AnswersRepo(s)
        ans = answers.get(answer_id)
        if ans is None:
            return "Sorry—this context expired. Please ask again.", False, 0

        items = ans.recommendations_json or []
        page = items[offset : offset + 3]
        shown = len(page)
        next_offset = offset + shown
        has_more = next_offset < min(12, len(items))

        # Render using the same format (cutoff + citations/dates); simplified list here.
        from tgbot.telegram.markdown_v2 import escape_markdown_v2
        from tgbot.time.formatters import format_ist_minute, format_date_ist

        lines = []
        lines.append(f"*{escape_markdown_v2('More recommendations')}*")
        lines.append(f"_Based on messages up to {escape_markdown_v2(format_ist_minute(ans.cutoff_ts))} (IST)_")
        lines.append("")
        for idx, r in enumerate(page, start=offset + 1):
            lines.append(f"*{idx}.* {escape_markdown_v2(r.get('title') or r.get('provider_key') or '')}")
            contacts = r.get("contacts") or []
            if contacts:
                lines.append(f"  - {escape_markdown_v2('Contact')}: {escape_markdown_v2(', '.join(contacts))}")
            cits = r.get("citations") or []
            cit_parts = []
            for c in cits[:3]:
                ts = c.get("message_ts")
                date = ts[:10] if isinstance(ts, str) else ""
                mid = c.get("message_id")
                cit_parts.append(f"{escape_markdown_v2('msg ' + str(mid))} ({escape_markdown_v2(date)})")
            lines.append(f"  - {escape_markdown_v2('Citations')}: {escape_markdown_v2('; '.join(cit_parts) if cit_parts else 'n/a')}")

        return "\n".join(lines), has_more, shown

