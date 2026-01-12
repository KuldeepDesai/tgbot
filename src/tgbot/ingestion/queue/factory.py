from __future__ import annotations

from tgbot.config.settings import get_settings
from tgbot.ingestion.queue.azure_queue import AzureQueue
from tgbot.ingestion.queue.interface import Queue
from tgbot.ingestion.queue.local_queue import LocalDirQueue


def get_queue() -> Queue:
    settings = get_settings()
    if settings.tg_queue == "local":
        return LocalDirQueue(settings.tg_local_queue_dir)
    if settings.tg_queue == "azure":
        return AzureQueue()
    raise ValueError(f"Unknown TG_QUEUE: {settings.tg_queue}")

