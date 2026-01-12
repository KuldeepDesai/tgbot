from __future__ import annotations

from tgbot.logging.correlation import get_request_id
from tgbot.storage.db import db_session
from tgbot.storage.repos.answers_repo import AnswersRepo
from tgbot.storage.repos.audit_repo import AuditRepo


def parse_feedback_callback(data: str) -> tuple[str, str] | None:
    # feedback:<answer_id>:up|down
    if not data or not data.startswith("feedback:"):
        return None
    parts = data.split(":")
    if len(parts) != 3:
        return None
    answer_id = parts[1]
    kind = parts[2]
    if kind not in ("up", "down"):
        return None
    return answer_id, kind


def record_feedback_event(*, answer_id: str, kind: str, user_id: str | None, telegram_message_id: int | None) -> None:
    with db_session() as s:
        answers = AnswersRepo(s)
        audit = AuditRepo(s)
        ans = answers.get(answer_id)
        channel_id = ans.channel_id if ans else None
        audit.write(
            event_type="feedback.captured",
            correlation_id=get_request_id(),
            channel_id=channel_id,
            payload_json={
                "answer_id": answer_id,
                "kind": kind,
                "user_id": user_id,
                "telegram_message_id": telegram_message_id,
            },
        )

