---
date: 2026-01-12
author: Kuldeep
project: tgbot
status: draft
---

## Implementation Plan: tgbot (MVP)

This plan translates the finalized brainstorming decisions into a concrete build plan focused on **pluggable architecture**, **low ops**, and **enterprise-grade replayability**.

### Goals (MVP)

- **Telegram-native Q&A** in-channel with **synthesized-by-default** answers, always with **citations** and a **per-community cutoff time**.
- **Cost-optimized**: batch processing every **4 hours**, embeddings for **every** channel window; external APIs for LLM/safety/embeddings.
- **Enterprise replay**: immutable raw **data lake** (Azure Blob, pluggable) + full rebuild via **ops-only CLI**.
- **Safety/ethics**: quarantine and hard-filter quarantined/deleted content from answers; refuse flagged queries with supportive safe response.
- **Observability**: audit events A+B+C+D+E + per-community cost accounting (per-call + daily rollups).

---

## Architecture Overview (Concept → Default Tech)

### Pluggable interfaces (concept-first)

- **`EventBuffer`**: append + batch read/ack
- **`ObjectStore`** / **`DataLakeStore`**: write/read immutable blobs + manifests
- **`RelationalStore`**: Postgres via `DATABASE_URL` (no vendor lock-in)
- **`VectorStore`**: chunk upsert/query (Upstash now; replaceable)
- **`LLMClient`**: synthesis + safety classification + embeddings (provider-configurable)

### MVP defaults (can be swapped later)

- **EventBuffer**: Azure Storage Queue
- **Raw Lake**: Azure Blob Storage, JSONL dumps
- **Relational DB**: Aiven Postgres
- **Vector DB**: Upstash Vector

---

## System Workflow (End-to-End)

### Stage 0 — Webhook capture (thin, always-on)

**Telegram Bot webhook → EventBuffer**

- Receive update (`message`, `edited_message`, `message_reaction`, deletion signal if available).
- Emit an **event envelope** to Azure Storage Queue quickly (no heavy processing, no Postgres writes).

**Event envelope (JSON):**

- `event_id` (uuid)
- `received_ts`
- `source` (`bot_webhook` | `userbot_backfill`)
- `channel_id` / `chat_id`
- `event_type` (`message_new|message_edit|message_delete|reaction_update|...`)
- `message_id` (if applicable)
- `payload` (raw Telegram update JSON)
- `schema_version`

### Stage 1 — 4-hour consolidation to raw lake (timeboxed)

**Consolidator job (cron)**

- Pull events from EventBuffer.
- Group into **(channel_id, 4-hour window)** buckets.
- Write immutable JSONL blobs to Azure Blob:

`raw/channel/{channel_id}/YYYY/MM/DD/HH00-HH00+4h.jsonl`

Plus a small manifest per blob (JSON):

`raw/channel/{channel_id}/YYYY/MM/DD/HH00-HH00+4h.manifest.json`

Manifest includes:

- `schema_version`, `channel_id`, window start/end
- counts by `event_type`
- min/max `message_id` observed (best effort)
- blob checksum/etag

**Ordering:** best-effort only; downstream must be idempotent and “latest version wins”.

**Fan-out (decision):** consolidator enqueues one message per blob into a second Azure Storage Queue (e.g., `lake-files`) for parallel processing.

`lake-files` queue message (JSON):

- `task_id` (uuid)
- `channel_id`
- `window_start`, `window_end`
- `blob_url`
- `manifest_url`
- `manifest_etag` (or checksum)
- `schema_version`
- `created_ts`

### Stage 2 — Parallel file ingestion workers (fan-out)

Multiple workers ingest blobs concurrently (bounded by concurrency settings). Each worker:

- Claims a file task (from a `file_tasks` queue/table) with a lease/lock.
- Reads JSONL events for the window.
- Produces derived state in Postgres:
  - message latest state + deleted/quarantined flags
  - entities + edges (vendors/services + rule topics)
  - chunks for the 4-hour window (clean + optional quarantine)
  - answer caches / evidence packs
  - audit + cost events + daily rollups
- Upserts chunk embeddings to VectorStore (Upstash).

### Stage 3 — Serve queries (on-demand)

On a user query:

1. **Query safety gate**: if flagged → supportive refusal, stop.
2. **Scope**: query-scoped to current channel (MVP).
3. **Retrieve**: vector search over **chunk embeddings**.
4. **Filter/rank** in Postgres “graph” (edge tables):
   - dedupe by entity/topic
   - recency + unique recommenders
   - small boost from **unique reactors** (positive reactions)
   - hard-filter `quarantined=true` and `deleted=true`
   - down-rank attachment-only content vs text content
5. **Synthesize (default)** using LLM over a **small evidence pack** (10–30 messages), output citations + cutoff time.
6. Add Telegram-native 👍/👎 reactions for feedback.
7. Emit audit + cost events (per-call + daily rollup update).

### Stage 4 — Explain (flag-gated)

If community flag `explain_enabled=false` (default), do not show the button.

If enabled:

- show inline **Explain** button under answer
- on click, post in-channel explanation using cached evidence pack (no new retrieval unless cache missing)

### Stage 5 — Full rebuild (ops-only CLI)

Rebuild derives everything from raw lake blobs:

- wipe derived tables + vector index namespaces
- reprocess all lake files deterministically
- re-materialize daily rollups from cost events

---

## Postgres Schema (MVP draft)

### Core identity/config

- `communities(id, name, created_ts, ...)`
- `channels(id, telegram_chat_id, title, type, created_ts, last_seen_ts, ...)`
- `community_channels(community_id, channel_id, created_ts)`
- `community_flags(community_id, explain_enabled boolean default false, ...)`

### File processing + watermarks

- `lake_files(id, channel_id, window_start, window_end, blob_url, manifest_json, status, leased_until, attempts, created_ts, updated_ts)`
- `channel_cursors(channel_id, last_seen_message_id, last_seen_ts, updated_ts)`
- `community_cutoffs(community_id, cutoff_ts, updated_ts)` *(best-effort watermark; may lag per channel)*

### Message state (latest + versions)

- `messages(channel_id, message_id, sender_id, ts, text, attachment_metadata_json, has_text, deleted boolean, quarantined boolean, latest_version_ts, raw_ref, ...)`
- `message_versions(channel_id, message_id, version_ts, text, attachment_metadata_json, raw_ref, ...)` *(optional, can be capped)*

### Entities / rule topics / edges (“graph in SQL”)

- `entities(id, entity_type enum('vendor','service','rule_topic'), normalized_name, display_name, category, created_ts)`
- `message_entities(channel_id, message_id, entity_id, sentiment, extracted_contact, extracted_context, created_ts)`
- `entity_recommenders(entity_id, user_id, first_seen_ts, last_seen_ts)` *(derived)*
- `rule_topics(id, name, entity_id, ...)` *(optional; can use entities only)*

### Reactions / upvotes

> **Risk:** Telegram may not expose “unique reactors” reliably to bots; if not, we’ll approximate using available aggregate counts.

- `message_reaction_counts(channel_id, message_id, positive_reaction_count, updated_ts, raw_ref)`

### Chunks + embeddings

- `chunks(id, channel_id, window_start, window_end, blob_url, chunk_text, quarantined boolean, deleted_excluded boolean, created_ts)`
- `chunk_sources(chunk_id, channel_id, message_id)` *(citations mapping)*
- `vector_index_refs(chunk_id, vector_id, vector_store, updated_ts)` *(tracking for rebuild/debug)*

### Answers + evidence packs (for Explain)

- `answers(id, community_id, channel_id, user_id, query_text, answer_text, cutoff_ts, created_ts, cache_key, ...)`
- `answer_sources(answer_id, channel_id, message_id, rank, citation_text, ...)`

### Auditing + cost

- `audit_events(id, community_id, channel_id, user_id, event_type, event_ts, correlation_id, payload_json)`
- `cost_events(id, community_id, channel_id, purpose, provider, model, pricing_version, input_units, output_units, estimated_cost_usd, event_ts, correlation_id, payload_json)`
- `daily_cost_rollups(community_id, day, total_cost_usd, by_purpose_json, updated_ts)`

---

## Azure Storage Layout (MVP)

### Raw lake blobs (JSONL)

`raw/channel/{channel_id}/YYYY/MM/DD/HH00-HH00+4h.jsonl`

Each line: one event envelope JSON.

### Manifests

`raw/channel/{channel_id}/YYYY/MM/DD/HH00-HH00+4h.manifest.json`

---

## Concurrency, Idempotency, and Ordering

- **Best-effort ordering**: do not rely on queue order.
- **Idempotency keys**:
  - event_id unique
  - message identity: `(channel_id, message_id)`
  - lake file identity: `(channel_id, window_start, window_end)`
- **Leases/locks**:
  - `lake_files` row lease (`leased_until`) or Postgres advisory locks per file
- **“Latest wins”**:
  - edits/deletes/reactions update message state using newest `version_ts` observed

---

## Open technical risk to validate early

- **Reactions unique reactors**: verify Telegram API support; if not possible, use aggregate counts as tie-breaker.

