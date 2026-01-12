from __future__ import annotations

import asyncio
from dataclasses import dataclass

from fastapi import APIRouter
from pydantic import BaseModel

from tgbot.logging.correlation import get_request_id, request_id_scope
from tgbot.ops.cli.main import _send_message
from tgbot.storage.db import db_session
from tgbot.storage.repos.audit_repo import AuditRepo
from tgbot.storage.repos.channels_repo import ChannelsRepo

router = APIRouter()


class BroadcastRequest(BaseModel):
    text: str
    telegram_chat_id: str | None = None  # if set, send to one channel; else broadcast


@router.post("/broadcast")
def broadcast(req: BroadcastRequest):
    with request_id_scope():
        text = (req.text or "").strip()
        if not text:
            return {"error": {"code": "validation", "message": "text is required", "details": None}, "request_id": get_request_id()}

        with db_session() as s:
            channels = ChannelsRepo(s)
            audit = AuditRepo(s)

            targets = []
            if req.telegram_chat_id:
                ch = channels.get_by_telegram_chat_id(req.telegram_chat_id)
                if not ch:
                    return {"error": {"code": "not_found", "message": "channel not found", "details": None}, "request_id": get_request_id()}
                targets = [ch]
            else:
                targets = channels.list_all()

        async def _run():
            results = []
            for ch in targets:
                try:
                    await _send_message(ch.telegram_chat_id, text)
                    results.append({"channel_id": ch.id, "telegram_chat_id": ch.telegram_chat_id, "ok": True})
                except Exception as e:
                    results.append({"channel_id": ch.id, "telegram_chat_id": ch.telegram_chat_id, "ok": False, "error": str(e)})
            return results

        results = asyncio.run(_run())

        with db_session() as s2:
            AuditRepo(s2).write(
                event_type="ops.http.broadcast",
                correlation_id=get_request_id(),
                channel_id=None,
                payload_json={"results": results},
            )

        return {"data": {"results": results}, "request_id": get_request_id()}

