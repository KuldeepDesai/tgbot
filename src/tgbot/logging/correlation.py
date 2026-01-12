from __future__ import annotations

import contextvars
import uuid

_request_id_var: contextvars.ContextVar[str] = contextvars.ContextVar("request_id", default="")


def new_request_id() -> str:
    return str(uuid.uuid4())


def get_request_id() -> str:
    rid = _request_id_var.get()
    if rid:
        return rid
    rid = new_request_id()
    _request_id_var.set(rid)
    return rid


def set_request_id(request_id: str) -> None:
    _request_id_var.set(request_id)


class request_id_scope:
    def __init__(self, request_id: str | None = None):
        self.request_id = request_id or new_request_id()
        self._token: contextvars.Token[str] | None = None

    def __enter__(self):
        self._token = _request_id_var.set(self.request_id)
        return self.request_id

    def __exit__(self, exc_type, exc, tb):
        if self._token is not None:
            _request_id_var.reset(self._token)

