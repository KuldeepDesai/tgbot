from __future__ import annotations

from tgbot.config.settings import get_settings
from tgbot.lake.object_store.azure_blob import AzureBlobObjectStore
from tgbot.lake.object_store.interface import ObjectStore
from tgbot.lake.object_store.local_file import LocalFileObjectStore


def get_object_store() -> ObjectStore:
    settings = get_settings()
    if settings.tg_object_store == "local":
        return LocalFileObjectStore(settings.tg_local_lake_dir)
    if settings.tg_object_store == "azure":
        return AzureBlobObjectStore()
    raise ValueError(f"Unknown TG_OBJECT_STORE: {settings.tg_object_store}")

