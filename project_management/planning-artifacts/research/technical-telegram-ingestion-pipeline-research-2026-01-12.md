---
stepsCompleted: [1, 2, 3, 4, 5]
inputDocuments:
  - project_management/planning-artifacts/product-brief-tgbot-2026-01-12.md
  - project_management/analysis/brainstorming-session-2026-01-12.md
workflowType: 'research'
lastStep: 5
research_type: 'technical'
research_topic: 'Telegram ingestion + replayable pipeline for synthesized Q&A (Bot API + Client API/userbot), Azure Queue/Blob raw lake, Postgres + Vector DB derived indexes'
research_goals: 'Validate platform constraints (history/backfill, edits/deletes, reactions, permalinks), confirm feasibility of chosen pipeline (Azure Storage Queue → Blob JSONL → parallel workers), and identify high-risk unknowns to test before coding.'
user_name: 'Kuldeep'
date: '2026-01-12'
web_research_enabled: true
source_verification: partial
---

# Technical Research: Telegram Ingestion + Replayable Q&A Pipeline

**Date:** 2026-01-12  
**Author:** Kuldeep  
**Research Type:** technical  

## Executive Summary

We are building an enterprise-grade, low-ops pipeline that ingests Telegram conversations, produces synthesized answers with citations, and supports full rebuilds and future multi-channel/multimodal expansion. The architecture is **Logstash-like**: webhook → **Azure Storage Queue** (event buffer) → **4-hour consolidated JSONL** in **Azure Blob raw lake** → **parallel workers** ingest files into **Postgres (Aiven)** + **Vector DB (Upstash)**.

Key technical risks to validate early:

- **Backfill feasibility**: Bot API does not provide robust historical history retrieval; backfill must use **Telegram Client API** via a system-owned userbot. (Telegram API method reference: `messages.getHistory` on core Telegram API docs: `https://core.telegram.org/method/messages.getHistory`)
- **Reaction semantics**: Confirm what Bot API exposes for reactions (counts vs per-user). Primary docs to validate: `Update` object and reaction-related update types on `https://core.telegram.org/bots/api`.
- **Deletion signals**: Confirm whether and how deletions are delivered to bots; if not, we treat deletes as “best-effort” derived state and avoid citing deleted messages by periodically reconciling via userbot.
- **Permalink robustness**: Clickable permalinks are “best effort”; MVP supports fallback citations (channel + date + message_id). Link formats must be validated per Telegram docs/behavior.

## Table of Contents

1. Architecture recap and invariants  
2. Telegram platform constraints to validate (Bot API vs Client API)  
3. Ingestion and replay design (Queue → Blob → Workers)  
4. Citation/link strategy (best-effort permalinks, fallback)  
5. Message lifecycle (edit/delete) + reactions (upvote boost)  
6. Recommended early spike tests (before implementation)  

---

## 1) Architecture recap and invariants

Non-negotiable system invariants from brainstorming/product brief:

- **Synthesized-by-default** answers in-channel, with **citations** and **cutoff time**.
- **Query-scoped** (current channel only) for MVP to prevent info leakage.
- **Safety**: quarantined content never used in answers; flagged queries refuse and stop.
- **Replayability**: raw lake is immutable source-of-truth; full rebuild via ops-only CLI.
- **Pluggability**: Postgres/vector/object store/event buffer are adapters behind interfaces.

---

## 2) Telegram platform constraints to validate (Bot API vs Client API)

### 2.1 Bot API capabilities (update-driven)

Bots primarily operate on **updates** delivered via polling (`getUpdates`) or webhooks (`setWebhook`). The canonical reference for update payloads and supported fields is the Bot API docs:

- `https://core.telegram.org/bots/api`

**What we must validate from docs:**

- Which update fields exist for:
  - message edits (`edited_message` is commonly supported)
  - reactions (whether there are reaction updates and what they contain)
  - deletions (whether any “message deleted” update exists)

### 2.2 Client API capabilities (history/backfill)

For true history/backfill, we rely on Telegram’s **Client API** (user account), not Bot API. The core primitive to validate/lean on is:

- `messages.getHistory`: `https://core.telegram.org/method/messages.getHistory`

This supports paging through chat history and enables a per-channel cursor strategy such as `last_seen_message_id`.

**Operational implication:** userbot credential/session handling becomes a critical ops concern (secrets, account access, rate limiting).

---

## 3) Ingestion + replay design (Queue → Blob → Workers)

### 3.1 Event buffer: Azure Storage Queue

MVP uses Azure Storage Queue as the event buffer because it’s low-cost and simple. We will treat it as **at-least-once** delivery and build idempotent processing.

Primary docs to consult/validate during implementation:

- Azure Storage Queues overview / REST/SDK docs on `https://learn.microsoft.com/` (search “Azure Storage queues message size”, “visibility timeout”, “message retention”).

### 3.2 Raw lake: Azure Blob JSONL

Every 4 hours, per channel, we consolidate queue events into immutable JSONL blobs + manifest. This makes:

- replay/rebuild deterministic
- vendor swaps practical (new Postgres provider, new vector DB, future graph DB)
- future multimodal feasible (store attachments once, process later)

### 3.3 Parallel workers (multiple files simultaneously)

We chose fan-out via a second queue (`lake-files`) so that multiple workers can process multiple blobs concurrently without polling Postgres. Each worker still writes a `lake_files` status row in Postgres for idempotency/leases.

### 3.4 Ordering

We accepted **best-effort ordering**. Downstream applies:

- idempotency via event_id + (channel_id,message_id)
- “latest version wins” for edits/deletes/reactions

---

## 4) Citations / permalinks strategy

MVP supports:

- **Best-effort permalinks** when feasible (Telegram link formats vary by public/private contexts).
- **Fallback citation** when links aren’t available: `channel_name + date + message_id` (optionally sender).

Primary docs/behavior references to validate:

- Bot API `Message` identifiers and chat identifiers in `https://core.telegram.org/bots/api`
- Telegram message link behavior depends on chat type and settings (validate empirically in a spike test).

---

## 5) Message lifecycle + reactions (“upvotes”)

### 5.1 Edits

Policy: store versions (optional) and use latest for retrieval/synthesis; never cite earlier versions if a later edit exists.

### 5.2 Deletes

Policy: keep content stored for replay/debug, but never use deleted messages in answers.

**Risk:** If Bot API does not provide reliable deletion signals, we need a reconciliation strategy (periodic userbot sweep) to discover deletions and mark them.

### 5.3 Reactions / upvotes

We decided:

- treat any “positive” reaction as an upvote
- use upvotes as **small tie-breaker boost**
- count **unique reactors** (anti-gaming)
- apply across vendors and rule topics

**Risk:** confirm whether Bot API exposes unique reactor identities or only aggregate counts. If only counts are available, we degrade gracefully to aggregate counts as the tie-breaker.

---

## 6) Recommended early spike tests (before implementation)

These are short, high-signal tests to run immediately:

1. **Bot API update coverage**: verify what updates arrive for edits, reactions, and deletions in your target chat types (group/supergroup/channel).
2. **Userbot history backfill**: validate paging speed/limits with `messages.getHistory` and confirm cursor strategy.
3. **Permalink feasibility**: validate whether your groups/channels have stable clickable message links; document fallback format for private contexts.
4. **Queue→Blob consolidation**: run a simulated flow (100k events) to validate throughput and blob layout ergonomics.

