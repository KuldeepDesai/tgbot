from __future__ import annotations

import json
import logging
import sys
from datetime import datetime, timezone
from typing import Any

from tgbot.logging.correlation import get_request_id


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, Any] = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname.lower(),
            "logger": record.name,
            "message": record.getMessage(),
            "request_id": getattr(record, "request_id", None) or get_request_id(),
        }
        if hasattr(record, "event"):
            payload["event"] = getattr(record, "event")
        if hasattr(record, "channel_id") and getattr(record, "channel_id") is not None:
            payload["channel_id"] = getattr(record, "channel_id")
        if record.exc_info:
            payload["exc_info"] = self.formatException(record.exc_info)
        # Attach extra structured fields (best-effort)
        extra = getattr(record, "extra", None)
        if isinstance(extra, dict):
            payload.update(extra)
        return json.dumps(payload, ensure_ascii=False)


def get_logger(name: str, *, service: str | None = None) -> logging.Logger:
    logger = logging.getLogger(name)
    if getattr(logger, "_tgbot_configured", False):
        return logger

    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter())
    logger.addHandler(handler)
    logger.propagate = False
    setattr(logger, "_tgbot_configured", True)

    if service:
        logger = logging.LoggerAdapter(logger, {"service": service})  # type: ignore[assignment]
    return logger

