from __future__ import annotations

from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from tgbot.storage.models.answers import Answer


class AnswersRepo:
    def __init__(self, session: Session):
        self.session = session

    def create(
        self,
        *,
        channel_id: str,
        query_text: str,
        cutoff_ts: datetime,
        recommendations_json: list,
        telegram_message_id: int | None = None,
    ) -> Answer:
        ans = Answer(
            channel_id=channel_id,
            query_text=query_text,
            cutoff_ts=cutoff_ts,
            recommendations_json=recommendations_json,
            telegram_message_id=telegram_message_id,
        )
        self.session.add(ans)
        self.session.flush()
        return ans

    def get(self, answer_id: str) -> Answer | None:
        return self.session.scalar(select(Answer).where(Answer.id == answer_id))

    def set_telegram_message_id(self, answer_id: str, telegram_message_id: int) -> None:
        ans = self.get(answer_id)
        if ans is None:
            raise KeyError("answer not found")
        ans.telegram_message_id = telegram_message_id
        self.session.add(ans)
        self.session.flush()

    def get_by_telegram_message_id(self, telegram_message_id: int) -> Answer | None:
        return self.session.scalar(select(Answer).where(Answer.telegram_message_id == telegram_message_id))

