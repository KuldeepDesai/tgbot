# tgbot

Telegram in-channel Q&A bot with a replayable ingestion pipeline.

This repo is scaffolded to follow `project_management/planning-artifacts/architecture.md`.

## Quick start (local)

1. Copy env template:

```bash
cp .env.example .env
```

2. Create a Postgres database and set `DATABASE_URL` in `.env`.

3. Run migrations (alembic):

```bash
alembic upgrade head
```

4. Register a channel:

```bash
python -m tgbot.ops.cli.main register-channel --telegram-chat-id <chat_id> --disclaimer-text "..."
```

5. Run receiver (long polling):

```bash
python -m tgbot.main.receiver
```

## Processes

- `receiver`: Telegram long-polling receiver → normalize updates → enqueue event envelopes
- `consolidator`: queue drain → write immutable raw-lake JSONL + manifest
- `worker`: process lake files → derive latest message state + safety flags
- `ops_api`: internal-only ops HTTP for broadcast/messaging

