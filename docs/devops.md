# DevOps Architecture (Docker-first)

## Goals

- **Docker-first runtime**: every long-running process runs as a container image.
- **Local before deploy**: you can run the exact same entrypoints locally, then validate the same behavior via Docker before deploying.
- **12-factor config**: everything is configured via environment variables (`.env` for local/dev).

## Services (process model)

The application is intentionally split into independent processes:

- **receiver**: `python -m tgbot.main.receiver`
- **consolidator**: `python -m tgbot.main.consolidator`
- **worker**: `python -m tgbot.main.worker`
- **ops_api**: `python -m tgbot.main.ops_api`

This maps 1:1 to `docker-compose.yml` services.

## State model

- **Database**: Postgres (container in dev; managed service in prod)
  - Env: `DATABASE_URL`
  - Migrations: `alembic upgrade head` (run as one-shot `migrate` container in compose)
- **Queue / Lake**:
  - Dev default uses **local directory** implementations.
  - In containers, these are mapped to persistent volumes:
    - `TG_LOCAL_QUEUE_DIR=/data/queue`
    - `TG_LOCAL_LAKE_DIR=/data/lake`
  - In production, switch to managed backends (e.g., Azure) via:
    - `TG_QUEUE=azure`
    - `TG_OBJECT_STORE=azure`

## Local run vs Docker run

Both are supported and intentionally equivalent:

- **Local**: run `python -m tgbot.main.<process>` directly.
- **Docker**: run the same module via a container image.

If something works locally but not in Docker, treat it as a deployment bug and fix the image/runtime until they match.

## Conventions

- **Images**: built from the repo root `Dockerfile`.
- **Compose**: `docker-compose.yml` is the canonical dev stack.
- **Secrets**: never commit `.env`; start from `env.example`.

