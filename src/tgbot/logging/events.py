from __future__ import annotations

from typing import Any

from tgbot.logging.correlation import get_request_id


def log_event(logger, event: str, *, channel_id: str | None = None, **fields: Any) -> None:
    """
    Standard structured log helper.
    """
    extra: dict[str, Any] = {"event": event, "request_id": get_request_id(), "extra": fields}
    if channel_id is not None:
        extra["channel_id"] = channel_id
    logger.info(event, extra=extra)

