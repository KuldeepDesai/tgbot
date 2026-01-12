from __future__ import annotations

import hashlib
import os

from tgbot.lake.object_store.interface import ObjectStore


class LocalFileObjectStore(ObjectStore):
    def __init__(self, root_dir: str):
        self.root_dir = root_dir
        os.makedirs(self.root_dir, exist_ok=True)

    def _abs(self, path: str) -> str:
        path = path.lstrip("/")
        return os.path.join(self.root_dir, path)

    def exists(self, path: str) -> bool:
        return os.path.exists(self._abs(path))

    def put_bytes(self, path: str, data: bytes) -> str:
        abs_path = self._abs(path)
        os.makedirs(os.path.dirname(abs_path), exist_ok=True)
        if os.path.exists(abs_path):
            # Immutable-by-default: caller should check exists() first. We still avoid overwriting.
            raise FileExistsError(path)
        with open(abs_path, "wb") as f:
            f.write(data)
        return hashlib.sha256(data).hexdigest()[:16]

    def get_bytes(self, path: str) -> bytes:
        with open(self._abs(path), "rb") as f:
            return f.read()

