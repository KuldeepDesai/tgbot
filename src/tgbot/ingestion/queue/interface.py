from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class QueueMessage:
    message_id: str
    body: str


class Queue:
    def enqueue(self, body: str) -> str:
        raise NotImplementedError

    def dequeue_batch(self, *, max_messages: int) -> list[QueueMessage]:
        raise NotImplementedError

    def delete(self, message_id: str) -> None:
        raise NotImplementedError

