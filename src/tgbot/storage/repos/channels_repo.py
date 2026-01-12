from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from sqlalchemy import select
from sqlalchemy.orm import Session

from tgbot.storage.models.channels import Channel


ChannelUpsertAction = Literal["created", "updated"]


@dataclass(frozen=True)
class UpsertResult:
    channel: Channel
    action: ChannelUpsertAction


class ChannelsRepo:
    def __init__(self, session: Session):
        self.session = session

    def get_by_telegram_chat_id(self, telegram_chat_id: str) -> Channel | None:
        return self.session.scalar(select(Channel).where(Channel.telegram_chat_id == telegram_chat_id))

    def get_by_id(self, channel_id: str) -> Channel | None:
        return self.session.get(Channel, channel_id)

    def list_all(self) -> list[Channel]:
        return list(self.session.scalars(select(Channel).order_by(Channel.created_at.asc())))

    def upsert_channel(self, *, telegram_chat_id: str, disclaimer_text: str) -> UpsertResult:
        existing = self.get_by_telegram_chat_id(telegram_chat_id)
        if existing is None:
            ch = Channel(telegram_chat_id=telegram_chat_id, disclaimer_text=disclaimer_text)
            self.session.add(ch)
            self.session.flush()
            return UpsertResult(channel=ch, action="created")

        changed = existing.disclaimer_text != disclaimer_text
        existing.disclaimer_text = disclaimer_text
        self.session.add(existing)
        self.session.flush()
        return UpsertResult(channel=existing, action="updated" if changed else "updated")

    def set_ingestion_enabled(self, channel_id: str, enabled: bool) -> None:
        ch = self.get_by_id(channel_id)
        if ch is None:
            raise KeyError("channel not found")
        ch.ingestion_enabled = enabled
        self.session.add(ch)
        self.session.flush()

