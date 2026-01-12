from __future__ import annotations

from tgbot.ingestion.queue.interface import Queue, QueueMessage


class AzureQueue(Queue):
    """
    Placeholder adapter for Azure Storage Queue.
    This is intentionally minimal; for local dev use LocalDirQueue.
    """

    def __init__(self, *args, **kwargs):
        raise NotImplementedError("AzureQueue adapter not implemented in this sandbox")

    def enqueue(self, body: str) -> str:  # pragma: no cover
        raise NotImplementedError

    def dequeue_batch(self, *, max_messages: int) -> list[QueueMessage]:  # pragma: no cover
        raise NotImplementedError

    def delete(self, message_id: str) -> None:  # pragma: no cover
        raise NotImplementedError

