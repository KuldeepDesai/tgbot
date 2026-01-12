---
stepsCompleted: [1, 2, 3, 4, 5, 6, 7, 8]
inputDocuments:
  - project_management/planning-artifacts/prd.md
  - project_management/planning-artifacts/product-brief-tgbot-2026-01-12.md
  - project_management/planning-artifacts/research/technical-telegram-ingestion-pipeline-research-2026-01-12.md
  - project_management/analysis/brainstorming-session-2026-01-12.md
  - project_management/planning-artifacts/implementation-plan-tgbot-2026-01-12.md
workflowType: architecture
project_name: tgbot
user_name: Kuldeep
date: 2026-01-12
lastStep: 8
status: complete
completedAt: 2026-01-12
---

# Architecture Decision Document

_This document builds collaboratively through step-by-step discovery. Sections are appended as we work through each architectural decision together._

## Project Context Analysis

### Requirements Overview

**Functional Requirements (architectural implications):**

- **Channel onboarding & configuration**
  - Register channels and persist channel metadata + per-channel disclaimer.
  - Associate incoming Telegram updates with a known channel record for multi-channel operation.
  - Operator workflows are CLI/log-driven (no admin UI for MVP).

- **Ingestion, backfill, and message lifecycle**
  - Ingest new messages continuously; support historical backfill.
  - Persist message metadata (chat/channel id, message id, user id, timestamp).
  - Handle edits (latest version wins) and deletions (tombstone + exclude from evidence).
  - Retain stored data indefinitely (manual deletion outside system).

- **Question detection & intake**
  - Treat a text message as a query only when it’s a bot mention or reply-to-bot (per PRD).
  - `/help` returns usage + per-channel disclaimer.

- **Answer generation & presentation**
  - Reply in-thread in the same channel, MarkdownV2 formatted.
  - Always include: citations (link when possible, fallback otherwise), dates, and a cutoff timestamp line “Based on messages up to … (IST)”.
  - Extract contacts only when present in evidence; never fabricate.

- **Recommendation exploration (“More recommendations”)**
  - Inline button paginates +3 results per click up to 12 distinct.
  - Pagination must preserve citations/dates/cutoff formatting and must not consume daily quota.

- **Quota management**
  - Enforce per-channel quota: 50 questions/day; reset at midnight IST.
  - Quota exceeded response is explicit and consistent.

- **Feedback capture**
  - Record 👍/👎 reactions on bot answers as feedback events.

- **Safety & guardrails**
  - Query safety gate: flagged queries refuse and stop.
  - Content safety: quarantine flagged ingested content; hard-filter quarantined content from retrieval/synthesis/citations.

- **Bot membership/permissions + audit events**
  - If bot removed / permissions reduced (when detectable), record audit event and stop or degrade ingestion to avoid noisy failure loops.

- **Operator messaging (out-of-band)**
  - Ops CLI + internal-only HTTP endpoint to broadcast or message a specific channel.

- **Failure handling**
  - Always fail gracefully with a “try again later” response when processing fails.

**Non-Functional Requirements (architecture shapers):**

- **Performance**
  - MVP avg latency < 5s; P95 ≤ 15s.
  - Show immediate “typing…” during processing.

- **Security**
  - Channel isolation is a hard requirement (no cross-channel leakage).
  - Secrets must not appear in logs or bot responses.
  - Ops-only HTTP endpoint should be network-restricted (MVP), not publicly exposed.

- **Reliability**
  - Degrade gracefully on failures; retries/backoff for Telegram variability.
  - Idempotent ingestion/processing to tolerate at-least-once delivery.

- **Observability**
  - Structured logs + correlation IDs across ingestion → processing → answering.
  - Audit events for ingestion lifecycle, batch runs, safety actions, answers served, explain/feedback, and membership/permission changes.

- **Scalability (MVP target)**
  - Up to ~5 channels per instance with acceptable latency.

### Scale & Complexity

- Primary domain: Telegram in-channel Q&A + replayable ingestion pipeline.
- Complexity level: medium (multi-component pipeline + safety + strict isolation + citations).
- Estimated architectural components: ~8–12
  - Telegram update receiver (polling or webhook)
  - Optional userbot backfill subsystem
  - Event buffer + consolidator
  - Raw lake storage + file-task fanout
  - Processing workers (normalize/edit/delete/quarantine/entities/chunks/embeddings)
  - Stores (Postgres + vector)
  - Query handler (retrieve → rank → synthesize → format)
  - Ops tooling (broadcast, rebuild) + audit/cost accounting

### Technical Constraints & Dependencies

- Telegram Bot API constraints (update-driven, may not expose deletes/reactions fully).
- Telegram Client API likely required for backfill/history (userbot ops/security implications).
- Evidence/citation constraints: permalinks best-effort; fallback citation required.
- MarkdownV2 escaping correctness is mandatory.
- Timezone semantics: cutoff timestamp + quota reset at midnight IST (time handling must be explicit).
- Replayability requirement: immutable raw-lake as source-of-truth; derived state must be rebuildable.

### Cross-Cutting Concerns Identified

- **Isolation**: channel-scoped retrieval + hard enforcement against leakage.
- **Evidence-first UX**: citations + dates + cutoff on every answer.
- **Safety**: query gate + quarantined content exclusion + auditability.
- **Idempotency & ordering**: at-least-once delivery, best-effort ordering, “latest wins” for edits/deletes/reactions.
- **Cost controls**: caching, bounded evidence packs, usage/cost event logging.
- **Operational clarity**: CLI/log-first workflows; minimal moving parts for MVP.

## Starter Template Evaluation

### Primary Technology Domain

API/Backend: Telegram bot runtime + ingestion pipeline + background workers + ops tooling.

### Starter Options Considered

**Python-first (recommended)**

- Bot framework option: `aiogram` **3.24.0** (released Jan 2, 2026 on PyPI).
- Alternative bot framework option: `python-telegram-bot` **22.5** (released Sep 27, 2025 on PyPI).
- Client API (userbot/backfill) option: `Telethon` **1.42.0** (released Nov 6, 2025 on PyPI).
- Client API alternative observed: `Pyrogram` **2.0.106** (last released Apr 30, 2023 on PyPI) — looks stale relative to alternatives.

**TypeScript/Node-first (alternative)**

- Bot framework options:
  - `grammy` **1.39.2** (npm; last published 12 days ago per npm metadata).
  - `telegraf` **4.16.3** (npm; last published 2 years ago per npm metadata) — looks less active recently.

### Selected Starter: Python + `uv` + `aiogram` (+ `Telethon` for backfill)

**Rationale for Selection:**

- Aligns with the likely MVP requirement for **Telegram Client API backfill** (userbot) and ongoing catch-up.
- Keeps the core runtime fully **async** for Telegram + IO-heavy pipeline tasks.
- Puts bot + pipeline + ops tooling in one language (minimize cognitive overhead for a solo MVP).

**Initialization Command:**

```bash
# uv docs: "Usage: uv init [OPTIONS] [PATH]"
uv init tgbot
cd tgbot

# Bot runtime
uv add aiogram==3.24.0

# Userbot/backfill (Client API)
uv add Telethon==1.42.0

# (Additional dependencies will be added in implementation stories: Postgres client, Azure Queue/Blob SDKs,
# Upstash Vector client, HTTP server for ops endpoint, lint/test tooling, etc.)
```

**Architectural Decisions Provided by Starter:**

- **Language & Runtime**: Python async-first, single dependency manager (`uv`).
- **Build Tooling**: lightweight (no heavy app framework required to start).
- **Code Organization**: we will define module boundaries explicitly in the next steps (bot, ingestion, workers, storage adapters, query/answer).
- **Development Experience**: reproducible installs and fast local iteration via `uv`.

## Core Architectural Decisions

### Decision Priority Analysis

**Already decided (from PRD / planning docs / starter):**

- Language/runtime: Python async-first (starter: `uv` + `aiogram`).
- Bot framework: `aiogram==3.24.0`.
- Userbot/backfill library: `Telethon==1.42.0`.
- Primary DB: Postgres (managed; `DATABASE_URL`).
- Vector store: Upstash Vector (pluggable behind interface).
- Raw lake: Azure Blob (immutable JSONL).
- Event buffer: Azure Storage Queue.
- Channel isolation: hard requirement (no cross-channel leakage).
- Answer invariants: citations + dates + cutoff timestamp (IST) on every answer.
- Safety: query safety gate + quarantine; quarantined/deleted content excluded from answers.

**Critical decisions (block implementation if unclear):**

- Telegram update delivery shape: **Long polling** (PRD) vs **webhook → queue** (pipeline plan).
  - MVP default: **Long polling**, while still writing events into the same ingestion pipeline (queue/lake) once received.
- Backfill strategy: **Client API userbot required** (Bot API insufficient for history).

**Important decisions (shape architecture):**

- DB access + migrations: **SQLAlchemy 2.0.45 + alembic 1.18.0**.
- Ops-only HTTP endpoint: **FastAPI 0.128.0** (internal-only / network-restricted).
- Config management: **pydantic-settings 2.12.0** (env-first; supports secret backends later).

**Deferred decisions (post-MVP / can be revisited):**

- Cross-channel retrieval (explicitly post-MVP).
- Explain button (feature-flagged; default off).
- Dashboards/admin UI.

### Data Architecture

- **System of record**: Postgres (managed) for operational state:
  - channels/communities/config/flags
  - messages (latest state + optional versions)
  - tombstones for deletions + quarantine metadata
  - chunks + citation mappings
  - answers + feedback + audit + cost events
- **Raw source-of-truth**: Azure Blob raw lake storing immutable per-channel 4h JSONL + manifests.
- **Vector index**: Upstash Vector for chunk retrieval; must support per-channel namespace + rebuild.

### Authentication & Security

- **User auth**: none beyond Telegram membership boundary (MVP).
- **Authorization**:
  - answering is implicit by channel membership (no DM mode)
  - ops-only endpoint is network-restricted (no public exposure)
- **Isolation**: `channel_id` is a first-class mandatory filter in retrieval/ranking/synthesis.

### API & Communication Patterns

- **Inbound Telegram**: long polling receiver (MVP default) → normalize → enqueue event envelopes.
- **Internal modules communicate via**: in-process function calls + durable queues (Azure Storage Queue) for async fan-out.
- **Error handling**: consistent user-facing fallback; structured logs + correlation IDs.
- **Rate limiting**:
  - user-facing: per-channel daily quota (50/day, reset midnight IST)
  - internal: retries/backoff for Telegram + storage calls

### Infrastructure & Deployment

- **Deployment unit (MVP)**: one codebase, multiple processes (receiver / consolidator / workers / optional ops API), all sharing Postgres + Blob + Queue + Vector.
- **Replayability**: ops-only CLI can rebuild derived state from raw lake.

### Decision Impact Analysis

- This set of decisions locks the core shape: receive updates → durable event log → batch/parallel derive indexes → answer with strict scope + evidence.
- Main open risk to validate early: what Telegram exposes for deletes/reactions, and how permalink generation behaves in your target chat types (fallback citation when needed).

## Implementation Patterns & Consistency Rules

### Pattern Categories Defined

**Critical Conflict Points Identified:** 14 areas where AI agents could make different choices and break integration (naming, payload schemas, time handling, idempotency keys, folder boundaries, logging, error shapes, MarkdownV2 escaping, and DB migration patterns).

### Naming Patterns

**Database Naming Conventions (Postgres):**

- **Tables**: `snake_case` and **plural** (e.g., `channels`, `messages`, `audit_events`)
- **Columns**: `snake_case` (e.g., `channel_id`, `message_id`, `created_at`)
- **Primary keys**: `id` (uuid unless naturally keyed)
- **Natural keys**: explicitly defined (e.g., `messages` unique key `(channel_id, message_id)`)
- **Foreign keys**: `<referenced_table_singular>_id` (e.g., `channel_id`, `community_id`)
- **Timestamps**: `*_at` stored as UTC (e.g., `created_at`, `updated_at`)
- **Indexes**: `ix_<table>__<col1>__<col2>` (double-underscore separator)

**API Naming Conventions (ops-only HTTP):**

- Base path: `/ops/v1/...`
- JSON fields: `snake_case`
- Resource naming: plural nouns (`/channels`, `/communities`)
- IDs: always `..._id` in JSON (e.g., `channel_id`)
- HTTP status usage: standard (400 validation, 404 not found, 409 conflict, 500 unexpected)

**Code Naming Conventions (Python):**

- Modules/files: `snake_case.py`
- Classes: `PascalCase`
- Functions/vars: `snake_case`
- Constants: `UPPER_SNAKE_CASE`
- Enums: `PascalCase` names with `UPPER_SNAKE_CASE` values

### Structure Patterns

**Project organization (single repo, multi-process):**

- One codebase with separate entrypoints for:
  - `receiver` (Telegram long polling)
  - `consolidator` (queue → lake file writer)
  - `worker` (lake file processor)
  - `ops_api` (internal HTTP)
  - `cli` (ops-only commands: broadcast, rebuild, backfill trigger)

**Folder boundaries (agents must not “invent” new roots):**

- `src/tgbot/config/` — configuration + settings
- `src/tgbot/logging/` — JSON logging + correlation helpers
- `src/tgbot/telegram/` — Bot API integration (receiver, handlers, MarkdownV2)
- `src/tgbot/userbot/` — Client API (Telethon) backfill + reconciliation
- `src/tgbot/ingestion/` — event envelope schema, queue writer/reader, consolidator
- `src/tgbot/lake/` — blob paths/manifests, immutable file reader/writer
- `src/tgbot/storage/` — Postgres repositories + migrations + models
- `src/tgbot/vector/` — vector store adapter interface + Upstash implementation
- `src/tgbot/query/` — retrieve → rank → evidence pack → synthesize
- `src/tgbot/safety/` — query safety gate + message quarantine classifier
- `src/tgbot/ops/` — ops API routes + CLI command implementations
- `tests/` — unit/integration tests

**Test placement:**

- Tests live under `tests/` (not co-located), mirroring module paths.

### Format Patterns

**Event envelope (durable ingest contract):**

- All ingest events must be normalized into a single schema:
  - `event_id` (uuid)
  - `received_at` (UTC ISO8601)
  - `source` (`bot_api` | `userbot`)
  - `channel_id` (internal UUID) + `telegram_chat_id` (int/str as provided)
  - `event_type` (enum; e.g., `message_new`, `message_edit`, `message_delete`, `reaction_update`)
  - `message_id` (int when applicable)
  - `payload` (raw Telegram JSON)
  - `schema_version` (int)
- JSON keys are `snake_case`. No ad-hoc variants.

**API response format (ops-only HTTP):**

- Success: `{ "data": <payload>, "request_id": "<id>" }`
- Error: `{ "error": { "code": "<string>", "message": "<human>", "details": <obj|null> }, "request_id": "<id>" }`

**Date/time rules (avoid subtle bugs):**

- Persist all timestamps in **UTC**.
- Convert to **IST only at presentation time** for bot answers:
  - Always show: `Based on messages up to <cutoff> (IST)`
- Citation date formatting is fixed (single helper function).

**Telegram MarkdownV2 escaping:**

- Exactly one shared function: `escape_markdown_v2(text)`.
- All user-supplied and message-sourced strings must be escaped through it before sending.

### Communication Patterns

**Logging (structured, consistent):**

- JSON logs only.
- Every log line must include:
  - `level`, `ts` (UTC), `service` (receiver/worker/etc), `request_id` (correlation id), `channel_id` when applicable
- Use consistent event names (e.g., `ingest.enqueued`, `lake.written`, `worker.file_processed`, `answer.served`, `quota.exhausted`, `safety.query_refused`).

**Idempotency & “latest wins”:**

- Idempotency keys:
  - event: `event_id`
  - message: `(channel_id, message_id)`
  - lake file: `(channel_id, window_start, window_end)` or manifest checksum
- Edits/deletes/reactions apply “latest wins” using event timestamps (or Telegram edit date when provided).

### Process Patterns

**Error handling:**

- Receiver:
  - never crash on a single bad update; log and continue
  - always protect MarkdownV2 output
- Query path:
  - on failure: user gets the standard fallback message
  - internal logs capture exception with `request_id`

**Retry/backoff:**

- Network calls use exponential backoff with jitter.
- Never retry non-idempotent actions without idempotency keys.

### Enforcement Guidelines

**All AI Agents MUST:**

- Use the shared event envelope schema (no bespoke payload shapes).
- Treat `channel_id` filtering as mandatory for every retrieval/ranking/synthesis query.
- Store UTC; render IST only in bot output.
- Use the single MarkdownV2 escaping utility for all dynamic text.
- Emit structured logs with `request_id` and consistent event naming.

**Pattern enforcement:**

- If a change violates patterns, it must be accompanied by:
  - updating this section, and
  - a short justification in an ADR.

### Pattern Examples

**Good Examples:**

- Table: `messages` with unique constraint on `(channel_id, message_id)`
- Log event: `{"level":"info","event":"answer.served","request_id":"...","channel_id":"..."}`
- Bot output includes: `Based on messages up to 2026-01-12 16:00 (IST)`

**Anti-Patterns:**

- Storing IST timestamps in DB.
- Two different JSON shapes for the same event type.
- Mixing `camelCase` and `snake_case` across modules.
- Constructing MarkdownV2 manually in multiple places (escaping bugs).

## Project Structure & Boundaries

### Complete Project Directory Structure

```
tgbot/
├── README.md
├── pyproject.toml
├── uv.lock
├── .python-version
├── .gitignore
├── .env.example
├── scripts/
│   ├── dev_receiver.sh
│   ├── dev_worker.sh
│   ├── dev_ops_api.sh
│   └── fmt_lint_test.sh
├── migrations/
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
│       └── 0001_initial_schema.py
├── src/
│   └── tgbot/
│       ├── __init__.py
│       ├── config/
│       │   ├── __init__.py
│       │   ├── settings.py
│       │   └── secrets.py
│       ├── logging/
│       │   ├── __init__.py
│       │   ├── logger.py
│       │   ├── correlation.py
│       │   └── events.py
│       ├── time/
│       │   ├── __init__.py
│       │   ├── clocks.py
│       │   ├── tz.py
│       │   └── formatters.py
│       ├── telegram/
│       │   ├── __init__.py
│       │   ├── markdown_v2.py
│       │   ├── updates/
│       │   │   ├── __init__.py
│       │   │   ├── receiver_polling.py
│       │   │   └── normalization.py
│       │   ├── handlers/
│       │   │   ├── __init__.py
│       │   │   ├── help.py
│       │   │   ├── query.py
│       │   │   └── callbacks_more_recs.py
│       │   └── ui/
│       │       ├── __init__.py
│       │       ├── answer_format.py
│       │       └── keyboards.py
│       ├── userbot/
│       │   ├── __init__.py
│       │   ├── telethon_client.py
│       │   ├── backfill.py
│       │   └── reconcile.py
│       ├── ingestion/
│       │   ├── __init__.py
│       │   ├── schema/
│       │   │   ├── __init__.py
│       │   │   └── event_envelope.py
│       │   ├── queue/
│       │   │   ├── __init__.py
│       │   │   ├── interface.py
│       │   │   └── azure_queue.py
│       │   ├── consolidator/
│       │   │   ├── __init__.py
│       │   │   └── consolidate_to_lake.py
│       │   └── file_tasks/
│       │       ├── __init__.py
│       │       └── enqueue_lake_files.py
│       ├── lake/
│       │   ├── __init__.py
│       │   ├── paths.py
│       │   ├── manifest.py
│       │   ├── object_store/
│       │   │   ├── __init__.py
│       │   │   ├── interface.py
│       │   │   └── azure_blob.py
│       │   └── reader.py
│       ├── storage/
│       │   ├── __init__.py
│       │   ├── db.py
│       │   ├── models/
│       │   │   ├── __init__.py
│       │   │   ├── channels.py
│       │   │   ├── messages.py
│       │   │   ├── chunks.py
│       │   │   ├── answers.py
│       │   │   ├── audit_events.py
│       │   │   └── cost_events.py
│       │   ├── repos/
│       │   │   ├── __init__.py
│       │   │   ├── channels_repo.py
│       │   │   ├── messages_repo.py
│       │   │   ├── lake_files_repo.py
│       │   │   ├── quota_repo.py
│       │   │   └── audit_repo.py
│       │   └── migrations.md
│       ├── vector/
│       │   ├── __init__.py
│       │   ├── interface.py
│       │   └── upstash_vector.py
│       ├── safety/
│       │   ├── __init__.py
│       │   ├── query_gate.py
│       │   ├── message_classifier.py
│       │   └── quarantine_policy.py
│       ├── query/
│       │   ├── __init__.py
│       │   ├── retrieve.py
│       │   ├── rank.py
│       │   ├── evidence_pack.py
│       │   ├── synthesize.py
│       │   └── citations.py
│       ├── ops/
│       │   ├── __init__.py
│       │   ├── api/
│       │   │   ├── __init__.py
│       │   │   ├── app.py
│       │   │   └── routes/
│       │   │       ├── __init__.py
│       │   │       ├── broadcast.py
│       │   │       └── health.py
│       │   ├── cli/
│       │   │   ├── __init__.py
│       │   │   ├── main.py
│       │   │   ├── broadcast.py
│       │   │   ├── rebuild.py
│       │   │   └── backfill.py
│       │   └── internal_auth.md
│       ├── worker/
│       │   ├── __init__.py
│       │   ├── file_processor.py
│       │   ├── chunking.py
│       │   ├── embeddings.py
│       │   └── entity_extraction.py
│       └── main/
│           ├── __init__.py
│           ├── receiver.py
│           ├── consolidator.py
│           ├── worker.py
│           └── ops_api.py
└── tests/
    ├── unit/
    │   ├── test_markdown_v2.py
    │   ├── test_event_envelope_schema.py
    │   └── test_channel_isolation_filters.py
    └── integration/
        ├── test_worker_idempotency.py
        └── test_query_pipeline_smoke.py
```

### Architectural Boundaries

**API Boundaries:**

- Telegram Bot API boundary lives in `src/tgbot/telegram/` (only place that touches `aiogram` directly).
- Ops-only HTTP boundary lives in `src/tgbot/ops/api/` (only place that exposes internal HTTP routes).

**Component Boundaries:**

- `receiver` only normalizes Telegram updates and enqueues event envelopes.
- `consolidator` only drains queue + writes immutable raw lake files + enqueues file tasks.
- `worker` only reads lake files and writes derived state (Postgres + vector).
- `query` only reads derived indexes and produces answers with citations and cutoff timestamp.

**Service Boundaries:**

- Storage adapters are behind interfaces:
  - Queue: `src/tgbot/ingestion/queue/interface.py`
  - Object store: `src/tgbot/lake/object_store/interface.py`
  - Vector store: `src/tgbot/vector/interface.py`

**Data Boundaries:**

- Postgres is the operational “truth” for serving (messages latest state, chunks, entities, quota, audits).
- Azure Blob raw lake is the immutable replay source-of-truth.

### Requirements to Structure Mapping

**Feature/FR mapping:**

- Channel onboarding + disclaimers → `storage/models/channels.py`, `storage/repos/channels_repo.py`, `/ops/v1/...` routes
- Ingest new + edits + deletes → `telegram/updates/*` + `ingestion/schema/event_envelope.py` + `worker/file_processor.py`
- Backfill history → `userbot/backfill.py`
- Channel-scoped Q&A + citations/dates/cutoff → `query/*` + `telegram/ui/*`
- “More recommendations” pagination → `telegram/handlers/callbacks_more_recs.py` + `query/retrieve.py`
- Per-channel quota reset IST midnight → `storage/repos/quota_repo.py` + `time/*`
- Safety gate + quarantine → `safety/*` + worker quarantine flags in `storage/models/messages.py`
- 👍/👎 feedback capture → `telegram/handlers/*` + `storage/models/audit_events.py` (or dedicated feedback table later)
- Broadcast + internal endpoint → `ops/cli/*` + `ops/api/routes/broadcast.py`
- Replay/rebuild → `ops/cli/rebuild.py` + worker deterministic processing

**Cross-cutting concerns:**

- Correlation IDs + structured logs → `logging/*`
- MarkdownV2 escaping → `telegram/markdown_v2.py` (single implementation)
- UTC storage + IST rendering → `time/*`

### Integration Points

**Internal Communication:**

- Event envelope JSON is the durable contract between receiver and pipeline (`ingestion/schema/event_envelope.py`).
- Lake file manifest is the durable contract between consolidator and workers (`lake/manifest.py`).

**External Integrations:**

- Telegram Bot API (aiogram)
- Telegram Client API (Telethon)
- Azure Storage Queue + Azure Blob
- Postgres
- Upstash Vector
- LLM provider (safety + embeddings + synthesis), behind a client interface (added in implementation)

**Data Flow:**

Telegram update → normalize → enqueue envelope → consolidate to JSONL blob → enqueue file task → worker derives Postgres+vector → query handler retrieves+filters+formats answer.

### File Organization Patterns

**Configuration Files:**

- Env vars only; `.env.example` documents required variables.
- `config/settings.py` is the only place reading env vars into typed settings.

**Source Organization:**

- No new top-level folders beyond the ones listed above.
- Third-party SDK usage only inside adapter modules (queue/blob/vector/telegram/userbot).

**Test Organization:**

- Unit tests for formatting/schema rules.
- Integration tests for idempotency and query pipeline smoke.

### Development Workflow Integration

**Development server structure:**

- Run separate processes locally:
  - receiver
  - worker
  - ops_api
  - consolidator (cron-like)
- Single `request_id` flows through logs across processes.

**Build process structure:**

- Python package build via `pyproject.toml`.
- Migrations managed by alembic in `migrations/`.

**Deployment structure:**

- One repo, multiple process types sharing the same image/env config.

## Architecture Validation Results

### Coherence Validation ✅

**Decision Compatibility:**

- Chosen core libraries are compatible in principle: async Python bot (`aiogram`) + Client API (`Telethon`) + Postgres + Azure Queue/Blob + Vector store.
- Versions are recorded for the critical stack pieces we referenced (bot/userbot/framework/config/migrations).
- No internal contradictions in naming/time/idempotency rules.

**Pattern Consistency:**

- Naming rules are consistent across DB/API/code.
- Strong guardrails exist for the two biggest error-prone areas: **MarkdownV2 escaping** and **UTC storage vs IST rendering**.
- Event envelope contract + idempotency keys are clearly specified.

**Structure Alignment:**

- Directory structure matches the boundaries and enforces “SDK usage only in adapters”.
- Multi-process layout maps cleanly to the pipeline (receiver/consolidator/worker/query/ops).

### Requirements Coverage Validation ✅ (with a few notes)

**Functional Requirements Coverage:**

- Covered in architecture + structure:
  - in-channel threaded replies
  - Top-3 + “More recommendations”
  - citations + dates + cutoff timestamp
  - per-channel quota + IST reset
  - safety gate + quarantine + refusal
  - feedback capture
  - ops broadcast + internal endpoint
  - replay/rebuild from raw lake
  - channel isolation hard requirement

**Non-Functional Requirements Coverage:**

- Performance targets addressed via bounded evidence packs + caching + async IO.
- Reliability addressed via idempotency, “latest wins”, retries/backoff, durable event log.
- Observability addressed via structured logging + request/correlation IDs + audit/cost events.
- Security addressed via isolation + network-restricted ops endpoint + secrets hygiene.

### Implementation Readiness Validation ✅ (minor gaps)

**Decision Completeness:**

- Most core decisions are captured, but a few “implementation-critical” specifics are still implied rather than explicit:
  - How we generate / persist `channel_id` vs `telegram_chat_id` mapping at onboarding.
  - How we compute `cutoff_ts` (per-channel vs per-community) given the PRD’s “channel-scoped answers only” + the research doc’s “per-community cutoff” idea.

**Structure Completeness:**

- Tree is complete enough for agents to start without inventing folders.

**Pattern Completeness:**

- Strong core patterns. A couple small improvements would reduce ambiguity:
  - Explicit schema versioning policy for event envelope + lake manifest.
  - Explicit “deleted message detection” stance (best-effort via Bot API, reconcile via userbot sweep).

### Gap Analysis Results

**Critical Gaps:** none blocking.  
**Important Gaps:**

- Clarify **cutoff semantics**: per-channel vs per-community watermarking (and how displayed cutoff relates to channel scope).
- Clarify **onboarding flow**: how a channel is registered and how disclaimers are stored/updated.
- Clarify **permalink strategy**: how we decide link vs fallback citation at runtime.

**Nice-to-have gaps:**

- Add explicit “LLM client interface” module and naming (so agents don’t invent competing abstractions).
- Add minimal ADRs for the biggest decisions (polling vs webhook, backfill via userbot, cutoff semantics).

### Validation Issues Addressed

- None required changes; the above are mostly “make implicit explicit” improvements.

### Architecture Completeness Checklist

**✅ Requirements Analysis**

- [x] Project context thoroughly analyzed
- [x] Scale and complexity assessed
- [x] Technical constraints identified
- [x] Cross-cutting concerns mapped

**✅ Architectural Decisions**

- [x] Critical decisions documented with versions
- [x] Technology stack specified
- [x] Integration patterns defined
- [x] Performance considerations addressed

**✅ Implementation Patterns**

- [x] Naming conventions established
- [x] Structure patterns defined
- [x] Communication patterns specified
- [x] Process patterns documented

**✅ Project Structure**

- [x] Complete directory structure defined
- [x] Component boundaries established
- [x] Integration points mapped
- [x] Requirements to structure mapping complete

### Architecture Readiness Assessment

**Overall Status:** READY FOR IMPLEMENTATION  
**Confidence Level:** high

**Key Strengths:**

- Strong enforcement against agent divergence (patterns + directory boundaries).
- Replayable pipeline with clear idempotency strategy.
- Hard channel isolation baked into both architecture and patterns.

**Areas for Future Enhancement:**

- Tighten cutoff semantics + onboarding flow text.
- Add ADRs for the biggest decisions.

### Implementation Handoff

**AI Agent Guidelines:**

- Follow all architectural decisions exactly as documented
- Use implementation patterns consistently across all components
- Respect project structure and boundaries
- Refer to this document for all architectural questions

**First Implementation Priority:**

- Scaffold the repo using the Step 3 command:
  - `uv init tgbot`
  - add `aiogram==3.24.0` and `Telethon==1.42.0`
  - create the directory structure + migrations skeleton

## Architecture Completion Summary

### Workflow Completion

**Architecture Decision Workflow:** COMPLETED ✅  
**Total Steps Completed:** 8  
**Date Completed:** 2026-01-12  
**Document Location:** project_management/planning-artifacts/architecture.md

### Final Architecture Deliverables

**📋 Complete Architecture Document**

- All architectural decisions documented with specific versions
- Implementation patterns ensuring AI agent consistency
- Complete project structure with all files and directories
- Requirements to architecture mapping
- Validation confirming coherence and completeness

**🏗️ Implementation Ready Foundation**

- Key architectural decisions made across the workflow
- Implementation patterns defined to prevent agent conflicts
- Major architectural components specified (receiver / consolidator / worker / query / ops)
- MVP requirements supported end-to-end (scope isolation, citations/cutoff, safety, replayability)

**📚 AI Agent Implementation Guide**

- Technology stack with verified versions (where referenced)
- Consistency rules that prevent implementation conflicts
- Project structure with clear boundaries
- Integration patterns and communication standards

### Implementation Handoff

**For AI Agents:**
This architecture document is your complete guide for implementing tgbot. Follow all decisions, patterns, and structures exactly as documented.

**First Implementation Priority:**

- Initialize project using documented starter template:
  - `uv init tgbot`
  - add `aiogram==3.24.0` and `Telethon==1.42.0`
  - create the directory structure + migrations skeleton

**Development Sequence:**

1. Initialize project using documented starter template
2. Set up development environment per architecture
3. Implement core architectural foundations (event envelope, DB schema, adapters)
4. Build features following established patterns (ingest → derive → answer)
5. Maintain consistency with documented rules

### Quality Assurance Checklist

**✅ Architecture Coherence**

- [x] All decisions work together without conflicts
- [x] Technology choices are compatible
- [x] Patterns support the architectural decisions
- [x] Structure aligns with all choices

**✅ Requirements Coverage**

- [x] All functional requirements are supported
- [x] All non-functional requirements are addressed
- [x] Cross-cutting concerns are handled
- [x] Integration points are defined

**✅ Implementation Readiness**

- [x] Decisions are specific and actionable
- [x] Patterns prevent agent conflicts
- [x] Structure is complete and unambiguous
- [x] Examples are provided for clarity

---

**Architecture Status:** READY FOR IMPLEMENTATION ✅

**Next Phase:** Begin implementation using the architectural decisions and patterns documented herein.

**Document Maintenance:** Update this architecture when major technical decisions are made during implementation.


