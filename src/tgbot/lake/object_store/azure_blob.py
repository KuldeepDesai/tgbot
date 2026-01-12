from __future__ import annotations

from tgbot.lake.object_store.interface import ObjectStore


class AzureBlobObjectStore(ObjectStore):
    def __init__(self, *args, **kwargs):
        raise NotImplementedError("AzureBlobObjectStore adapter not implemented in this sandbox")

    def exists(self, path: str) -> bool:  # pragma: no cover
        raise NotImplementedError

    def put_bytes(self, path: str, data: bytes) -> str:  # pragma: no cover
        raise NotImplementedError

    def get_bytes(self, path: str) -> bytes:  # pragma: no cover
        raise NotImplementedError

