from __future__ import annotations

import os

from tgbot.config.settings import get_settings
from tgbot.lake.object_store.factory import get_object_store
from tgbot.storage.db import db_session
from tgbot.storage.repos.audit_repo import AuditRepo
from tgbot.storage.repos.messages_repo import MessagesRepo
from tgbot.worker.file_processor import process_lake_jsonl


def main() -> None:
    settings = get_settings()
    store = get_object_store()

    # Local MVP: scan for jsonl lake files and process them.
    root = settings.tg_local_lake_dir
    jsonl_paths: list[str] = []
    for dirpath, _dirnames, filenames in os.walk(root):
        for fn in filenames:
            if fn.endswith(".jsonl") and "/raw/" in (dirpath.replace("\\", "/") + "/"):
                # store paths are relative to root
                abs_path = os.path.join(dirpath, fn)
                rel_path = os.path.relpath(abs_path, root).replace("\\", "/")
                jsonl_paths.append(rel_path)

    with db_session() as s:
        msgs = MessagesRepo(s)
        audit = AuditRepo(s)
        for p in sorted(jsonl_paths):
            process_lake_jsonl(store=store, jsonl_path=p, messages_repo=msgs, audit_repo=audit)


if __name__ == "__main__":
    main()

