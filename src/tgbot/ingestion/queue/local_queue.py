from __future__ import annotations

import os
import uuid

from tgbot.ingestion.queue.interface import Queue, QueueMessage


class LocalDirQueue(Queue):
    """
    Very small local queue for dev/testing: each message is a file.
    Not safe for multi-process contention; good enough for MVP dev.
    """

    def __init__(self, directory: str):
        self.directory = directory
        os.makedirs(self.directory, exist_ok=True)

    def enqueue(self, body: str) -> str:
        mid = str(uuid.uuid4())
        path = os.path.join(self.directory, f"{mid}.msg")
        with open(path, "w", encoding="utf-8") as f:
            f.write(body)
        return mid

    def dequeue_batch(self, *, max_messages: int) -> list[QueueMessage]:
        files = sorted([fn for fn in os.listdir(self.directory) if fn.endswith(".msg")])[:max_messages]
        out: list[QueueMessage] = []
        for fn in files:
            mid = fn.removesuffix(".msg")
            path = os.path.join(self.directory, fn)
            try:
                with open(path, "r", encoding="utf-8") as f:
                    body = f.read()
            except FileNotFoundError:
                continue
            out.append(QueueMessage(message_id=mid, body=body))
        return out

    def delete(self, message_id: str) -> None:
        path = os.path.join(self.directory, f"{message_id}.msg")
        try:
            os.remove(path)
        except FileNotFoundError:
            return

