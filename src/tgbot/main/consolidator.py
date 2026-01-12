from __future__ import annotations

from tgbot.ingestion.consolidator.consolidate_to_lake import consolidate_once
from tgbot.ingestion.queue.factory import get_queue
from tgbot.lake.object_store.factory import get_object_store
from tgbot.storage.db import db_session
from tgbot.storage.repos.audit_repo import AuditRepo


def main() -> None:
    queue = get_queue()
    store = get_object_store()
    with db_session() as s:
        audit = AuditRepo(s)
        consolidate_once(queue=queue, store=store, audit=audit, max_messages=512)


if __name__ == "__main__":
    main()

