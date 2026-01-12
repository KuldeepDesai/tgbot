from __future__ import annotations


class ObjectStore:
    def exists(self, path: str) -> bool:
        raise NotImplementedError

    def put_bytes(self, path: str, data: bytes) -> str:
        """
        Writes bytes and returns an etag/checksum identifier.
        """
        raise NotImplementedError

    def get_bytes(self, path: str) -> bytes:
        raise NotImplementedError

