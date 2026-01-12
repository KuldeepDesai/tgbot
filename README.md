# tgbot

Telegram in-channel Q&A bot with a replayable ingestion pipeline.

This repo is scaffolded to follow `project_management/planning-artifacts/architecture.md`.

## Quick start (local)

1. Copy env template:

```bash
cp env.example .env
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

## Quick start (Docker)

All long-running processes are designed to run as Docker containers. For local development, `docker-compose.yml` runs:

- `postgres` (db)
- `migrate` (one-shot `alembic upgrade head`)
- `receiver` (Telegram long-polling)
- `consolidator` (queue → raw lake JSONL)
- `worker` (process raw lake → latest state)
- `ops_api` (internal ops HTTP API)

1. Copy env template and fill required values (at minimum `TELEGRAM_BOT_TOKEN`):

```bash
cp env.example .env
```

2. Build and start the stack:

```bash
docker compose up --build
```

3. (Optional) Run only a subset (example: db + receiver):

```bash
docker compose up --build postgres receiver
```

## Local before deploy

The “local” workflow and the Docker workflow use the **same entrypoints** (`python -m tgbot.main.<process>`). Recommended progression:

- Run locally to iterate fast (existing “Quick start (local)” steps)
- Run via Docker Compose to validate the deployable runtime image
- Deploy the same image(s) to your target environment

See `docs/devops.md` for the devops posture and conventions.

## Processes

- `receiver`: Telegram long-polling receiver → normalize updates → enqueue event envelopes
- `consolidator`: queue drain → write immutable raw-lake JSONL + manifest
- `worker`: process lake files → derive latest message state + safety flags
- `ops_api`: internal-only ops HTTP for broadcast/messaging

