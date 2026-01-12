---
stepsCompleted:
  - step-01-validate-prerequisites
  - step-02-design-epics
  - step-03-create-stories
  - step-04-final-validation
inputDocuments:
  - project_management/planning-artifacts/prd.md
  - project_management/planning-artifacts/architecture.md
  - project_management/planning-artifacts/implementation-plan-tgbot-2026-01-12.md
  - project_management/planning-artifacts/product-brief-tgbot-2026-01-12.md
  - project_management/planning-artifacts/research/technical-telegram-ingestion-pipeline-research-2026-01-12.md
  - project_management/analysis/brainstorming-session-2026-01-12.md
---

# tgbot - Epic Breakdown

## Overview

This document provides the complete epic and story breakdown for tgbot, decomposing the requirements from the PRD, UX Design if it exists, and Architecture requirements into implementable stories.

## Requirements Inventory

### Functional Requirements

FR1: System Operator can register a Telegram channel for use by the bot.  
FR2: System Operator can set a per-channel disclaimer text during onboarding.  
FR3: System Operator can update a channel’s disclaimer text via configuration (effective after app restart).  
FR4: System can associate incoming Telegram updates to a known channel record (for multi-channel operation).  

FR5: System can ingest new messages from each onboarded channel.  
FR6: System can backfill historical messages for an onboarded channel.  
FR7: System can persist ingested messages with message metadata (chat/channel id, message id, user id, timestamp).  
FR8: System can record message edits as updates to prior messages.  
FR9: System can record message deletions (when detectable) and prevent deleted messages from being used as evidence in answers.  
FR10: System can retain stored channel data indefinitely unless manually deleted outside the system.  

FR11: Busy Community Member can ask a question by mentioning the bot in a channel message.  
FR12: Busy Community Member can ask a question by replying to the bot in a channel thread.  
FR13: System can ignore messages that are neither a bot mention nor a reply-to-bot (not treated as a question).  
FR14: Busy Community Member can request usage instructions via `/help`.  

FR15: System can respond to a question with a threaded reply in the same channel.  
FR16: System can format answers using Telegram MarkdownV2.  
FR17: System can include Top 3 recommendations in an answer when applicable.  
FR18: System can include citations for answer content (Telegram message link when possible; fallback citation otherwise).  
FR19: System can include message dates alongside citations.  
FR20: System can include an “as-of cutoff” timestamp (IST) in every answer (e.g., “Based on messages up to … (IST)”).  
FR21: System can extract and display contact details when they are present in source messages.  
FR22: System can avoid fabricating contact details when none exist in sources.  
FR23: System can handle “conflicting recommendations” by presenting Top 3 while explicitly reflecting disagreement and supporting evidence.  

FR24: Busy Community Member can request more recommendations via an inline “More recommendations” button.  
FR25: System can return the next 3 distinct recommendations per click, up to 12 distinct total for the same question context.  
FR26: System can ensure “More recommendations” results preserve citations + dates + cutoff timestamp formatting.  
FR27: System can ensure “More recommendations” does not consume daily quota.  

FR28: System can enforce a per-channel daily question quota (default 50/day/channel).  
FR29: System can reset a channel’s quota at midnight India time.  
FR30: System can inform users when a channel’s daily quota is exhausted and refuse additional questions until reset.  

FR31: Busy Community Member can provide feedback on answers via 👍/👎 reactions on the bot’s answer message.  
FR32: System can record feedback events for later analysis.  

FR33: System can evaluate user queries against safety policies and refuse to answer when required.  
FR34: System can quarantine safety-flagged ingested content so it is excluded from normal answering.  

FR35: System can detect bot removal from a channel when Telegram provides such signals.  
FR36: System can detect bot permission changes when Telegram provides such signals.  
FR37: System can create an audit event when the bot is removed from a channel.  
FR38: System can create an audit event when the bot’s permissions change in a channel.  
FR39: System can stop ingesting from a channel after bot removal (or adjust behavior appropriately after permission loss).  

FR40: System Operator can send a message to a specific onboarded channel outside the normal Q&A flow.  
FR41: System Operator can broadcast a message to all onboarded channels outside the normal Q&A flow.  
FR42: System Operator can trigger out-of-band messaging via an ops CLI.  
FR43: System Operator can trigger out-of-band messaging via an internal-only HTTP endpoint.  

FR44: System can notify the user when it cannot produce an answer and ask them to try again later.  

### NonFunctional Requirements

NFR1 (Performance): Average end-to-end answer latency is < 5 seconds (MVP).  
NFR2 (Performance): P95 end-to-end answer latency is ≤ 15 seconds (MVP).  
NFR3 (Performance/UX): Bot must provide immediate processing feedback via Telegram “typing…” chat action.  
NFR4 (Reliability): System should degrade gracefully; if an answer cannot be produced, respond with a clear fallback rather than failing silently.  
NFR5 (Security): System must prevent cross-channel leakage; answers must only use evidence from the channel where the question was asked.  
NFR6 (Security): Provider API keys/secrets must not be exposed in logs or bot responses.  
NFR7 (Security): Ops/internal operator endpoint must be network-restricted (no additional auth required for MVP).  
NFR8 (Scalability): Support up to 5 onboarded channels per system instance while meeting latency targets.  
NFR9 (Integration): Telegram integration must be robust under normal API/network variability (retries/backoff as appropriate) without compromising channel isolation.  
NFR10 (Observability): Emit structured logs and include correlation IDs to support troubleshooting/auditing (quota, “bot not responding”, membership/permission changes).  

### Additional Requirements

- Starter stack (greenfield): Python async-first with `uv`, `aiogram` for Bot API, and `Telethon` for Client API backfill.
- Performance target clarification: PRD sets MVP avg latency < 5s; product brief targets < 3s avg. Treat < 5s as MVP hard target and < 3s as post-MVP optimization unless you decide otherwise.
- Delivery mode (MVP): long polling receiver for Telegram updates (still normalized into the same durable event/pipeline contract).
- Replayability: immutable raw lake is the source-of-truth; full rebuild must be possible via ops-only CLI.
- Pipeline shape: normalize incoming updates into an **event envelope** schema and write durably; consolidate into per-channel time-window JSONL blobs with manifests; process via parallel workers.
- Storage defaults (MVP): Postgres for operational state; Azure Storage Queue as event buffer; Azure Blob as raw lake; Upstash Vector for retrieval index (all adapters behind interfaces).
- Strict time rules: persist timestamps in UTC; render IST only at presentation time; every answer must include the fixed cutoff line “Based on messages up to … (IST)”.
- Strict formatting safety: a single shared Telegram MarkdownV2 escaping function must be used for all dynamic text to avoid broken rendering.
- Strict isolation: `channel_id` filtering is mandatory for every retrieval/ranking/synthesis path; no cross-channel evidence for MVP.
- Quota rules: per-channel daily quota 50/day; quota resets at midnight IST; “More recommendations” pagination must not consume quota.
- Safety: query safety gate must refuse flagged queries with a supportive safe response; quarantined content must be hard-filtered out of retrieval/synthesis/citations; keep audit metadata.
- Message lifecycle: handle edits as “latest wins”; treat deletions as best-effort (Bot API may not signal) and reconcile via userbot where needed; deleted messages must not be cited.
- Reactions: use reactions as a small ranking tie-breaker; prefer unique reactors when available; degrade gracefully to aggregate counts if Bot API does not expose unique reactors.
- Attachments: always ingest attachment metadata/pointers; down-rank attachment-only evidence; if top matches are attachments, disclose limitation (e.g., “I can’t read files yet in MVP.”).
- Trust signal clarification: product brief mentions a recency-weighted “confidence” signal, while brainstorming prefers no explicit confidence indicator in MVP. Default to trust via citations + dates + cutoff timestamp unless you want an explicit confidence line.
- Explainability (optional): “Explain” is feature-flagged per community, disabled by default; should reuse cached evidence packs to control cost.
- Ops tooling: CLI and internal-only HTTP endpoint for broadcast/per-channel messaging; replay/rebuild operations are ops-only (not bot commands).
- Observability + auditability: structured JSON logs with correlation/request IDs; audit events for ingestion lifecycle, batch runs, safety, answers served (sources), explain/feedback; cost events + daily rollups (if implemented).

### FR Coverage Map

FR1: Epic 1 — Register channel  
FR2: Epic 1 — Set disclaimer  
FR3: Epic 1 — Update disclaimer  
FR4: Epic 1 — Associate updates to channel record  
FR5: Epic 2 — Ingest new messages  
FR6: Epic 2 — Backfill history  
FR7: Epic 2 — Persist messages + metadata  
FR8: Epic 2 — Record edits  
FR9: Epic 2 — Record deletions (when detectable) + exclude from evidence  
FR10: Epic 2 — Retain data indefinitely  
FR11: Epic 3 — Ask via bot mention  
FR12: Epic 3 — Ask via reply-to-bot  
FR13: Epic 3 — Ignore non-question messages  
FR14: Epic 1 — `/help` usage instructions  
FR15: Epic 3 — Threaded replies  
FR16: Epic 3 — MarkdownV2 formatting  
FR17: Epic 3 — Top 3 recommendations  
FR18: Epic 3 — Citations (link or fallback)  
FR19: Epic 3 — Dates alongside citations  
FR20: Epic 3 — Cutoff timestamp line (IST)  
FR21: Epic 3 — Extract/display contacts when present  
FR22: Epic 3 — No fabricated contacts  
FR23: Epic 3 — Handle conflicting recommendations  
FR24: Epic 4 — “More recommendations” button  
FR25: Epic 4 — Next 3 per click up to 12 distinct  
FR26: Epic 4 — Preserve citations/dates/cutoff in pagination  
FR27: Epic 4 — Pagination does not consume quota  
FR28: Epic 4 — Per-channel daily quota enforcement  
FR29: Epic 4 — Reset quota midnight IST  
FR30: Epic 4 — Quota exhausted messaging + refusal  
FR31: Epic 5 — 👍/👎 feedback via reactions  
FR32: Epic 5 — Record feedback events  
FR33: Epic 5 — Query safety evaluation + refusal  
FR34: Epic 5 — Quarantine flagged ingested content from answering  
FR35: Epic 6 — Detect bot removal (when available)  
FR36: Epic 6 — Detect permission changes (when available)  
FR37: Epic 6 — Audit event on removal  
FR38: Epic 6 — Audit event on permission change  
FR39: Epic 6 — Stop/degrade ingestion after removal/permission loss  
FR40: Epic 6 — Ops message to a specific channel  
FR41: Epic 6 — Ops broadcast message  
FR42: Epic 6 — Trigger ops messaging via CLI  
FR43: Epic 6 — Trigger ops messaging via internal-only HTTP endpoint  
FR44: Epic 3 — “Try again later” failure handling  

## Epic List

### Epic 1: Onboard a community channel and make the bot usable
System Operator can register channels, set/update per-channel disclaimers, and users can discover usage via `/help`.
**FRs covered:** FR1, FR2, FR3, FR4, FR14

### Epic 2: Capture and maintain the community knowledge base (ingest + backfill + lifecycle)
System can ingest new messages, backfill history, persist message metadata, handle edits/deletes, and retain data.
**FRs covered:** FR5, FR6, FR7, FR8, FR9, FR10

### Epic 3: Ask questions in-channel and get evidence-backed answers (Top-3)
Busy Community Member can ask questions (mention/reply), and receive threaded, MarkdownV2 answers with Top-3, citations+dates+cutoff timestamp, contact extraction (no fabrication), conflict-aware formatting, and graceful failure fallback.
**FRs covered:** FR11, FR12, FR13, FR15, FR16, FR17, FR18, FR19, FR20, FR21, FR22, FR23, FR44

### Epic 4: Explore more results and enforce per-channel daily quota
Users can page “More recommendations” (+3 up to 12 distinct) without consuming quota; system enforces per-channel daily quota with IST reset and clear refusal messaging when exhausted.
**FRs covered:** FR24, FR25, FR26, FR27, FR28, FR29, FR30

### Epic 5: Safety and feedback loop
System enforces query safety refusal, quarantines unsafe ingested content from normal answering, and captures 👍/👎 feedback events on answers.
**FRs covered:** FR31, FR32, FR33, FR34

### Epic 6: Operate and troubleshoot the bot (membership/permissions, audit events, ops messaging)
System detects bot removal/permission changes where available, creates audit events, stops/degrades ingestion appropriately, and provides ops broadcast/per-channel messaging via CLI and internal-only HTTP endpoint.
**FRs covered:** FR35, FR36, FR37, FR38, FR39, FR40, FR41, FR42, FR43

## Epic 1: Onboard a community channel and make the bot usable

System Operator can register channels, set/update per-channel disclaimers, and users can discover usage via `/help`.

### Story 1.1: Set up initial project from the selected starter template
**FRs covered:** (Architecture prerequisite)

As a System Operator,
I want the project scaffolded using the approved architecture starter template,
So that the codebase is ready for implementing the bot and pipeline consistently.

**Acceptance Criteria:**

**Given** the architecture specifies Python + `uv` + `aiogram` + `Telethon` and a standard directory structure
**When** the project is initialized
**Then** the repo contains a Python project scaffold with dependency management in place (via `uv`)
**And** the bot and pipeline dependencies are added at the pinned versions specified in architecture (or documented equivalents if versions change).

**Given** the architecture defines standard module boundaries and entrypoints
**When** the scaffold is created
**Then** the project contains the expected source layout (e.g., `src/tgbot/...`), migrations skeleton, and runnable entrypoints for receiver/worker/ops.

### Story 1.2: Register a channel (ops CLI) with per-channel disclaimer
**FRs covered:** FR1, FR2, FR3

As a System Operator,
I want to register a Telegram channel (by `telegram_chat_id`) and set/update its disclaimer,
So that the bot can recognize the channel and show the correct disclaimer.

**Acceptance Criteria:**

**Given** I have access to the ops CLI and Postgres is reachable
**When** I run a command to register a channel with `telegram_chat_id` and `disclaimer_text`
**Then** the system creates a `channels` record (or updates the existing one) keyed by `telegram_chat_id`
**And** the command returns the saved channel identity (including internal `channel_id`) and a success status.

**Given** a channel is already registered
**When** I re-run the register command with the same `telegram_chat_id` and a new `disclaimer_text`
**Then** the system updates the stored disclaimer for that channel (idempotent upsert)
**And** the operator is informed that changes are effective after app restart (MVP behavior).

**Given** the operator passes invalid inputs (missing/empty disclaimer, invalid chat id format)
**When** the command runs
**Then** it fails with a clear validation error
**And** it does not create or modify any channel record.

**Given** structured logging is enabled
**When** a channel is created or updated
**Then** the system emits a structured log including `channel_id`, `telegram_chat_id`, action (`created`/`updated`), and a correlation/request id.

**Given** the system persists audit events to Postgres
**When** a channel is created or updated via the ops CLI
**Then** an `audit_events` record is written containing at least `event_type`, `event_ts`, `channel_id`, correlation/request id, and a small `payload_json` including `telegram_chat_id` and action (`created`/`updated`).

### Story 1.3: `/help` returns usage instructions + channel disclaimer (threaded)
**FRs covered:** FR14

As a Busy Community Member,
I want to use `/help` to see how to ask questions and the channel’s disclaimer,
So that I know how to use the bot correctly and safely.

**Acceptance Criteria:**

**Given** the bot is running in a registered channel
**When** a user sends `/help`
**Then** the bot replies as a threaded reply (reply-to the `/help` message)
**And** includes usage instructions (how to ask questions)
**And** includes the per-channel disclaimer text stored for that channel.

**Given** the bot is running in a channel that is not registered
**When** a user sends `/help`
**Then** the bot replies as a threaded reply with a safe, minimal message indicating the channel is not configured
**And** it does not leak any other channel’s disclaimer.

**Given** `/help` output contains dynamic text (disclaimer or other values)
**When** the bot renders the reply
**Then** all dynamic text is correctly escaped for Telegram MarkdownV2 (no broken formatting).

### Story 1.4: Resolve incoming updates to a known channel record
**FRs covered:** FR4

As the system,
I want to associate every incoming Telegram update to a known channel record (or ignore/log unknown channels),
So that multi-channel operation works reliably and safely.

**Acceptance Criteria:**

**Given** the receiver gets a Telegram update containing a `chat_id`
**When** the system looks up the channel by `telegram_chat_id`
**Then** it resolves the internal `channel_id` and attaches it to downstream processing for that update.

**Given** the receiver gets an update for an unregistered `chat_id`
**When** the system processes it
**Then** it does not ingest/process/store the message as normal content
**And** it records a structured log + `audit_events` entry indicating “unknown channel” with the `telegram_chat_id`
**And** it does not respond in-channel (silent by default for MVP).

### Story 1.5: Create minimal persistence for channels and audit events
**FRs covered:** (enables FR1–FR4 and audit persistence)

As a System Operator,
I want onboarding and audit events to be persisted in Postgres,
So that configuration and operational actions are durable and inspectable.

**Acceptance Criteria:**

**Given** the project has a migrations mechanism
**When** migrations are applied to a new database
**Then** the database has a `channels` table that can store (at minimum) `id` (internal `channel_id`), `telegram_chat_id` (unique), `disclaimer_text`, and timestamps
**And** the database has an `audit_events` table that can store (at minimum) `id`, `event_type`, `event_ts`, optional `channel_id`, `correlation_id`, and `payload_json`.

**Given** the `channels` table exists
**When** Story 1.1’s ops command upserts a channel
**Then** the data is persisted and readable on subsequent runs/restarts.

**Given** the `audit_events` table exists
**When** Story 1.1 or Story 1.3 records an audit event
**Then** the audit event is persisted and queryable by `event_type` and time range.

## Epic 2: Capture and maintain the community knowledge base (ingest + backfill + lifecycle)

System can ingest new messages, backfill history, persist message metadata, handle edits/deletes, and retain data.

### Story 2.1: Normalize Telegram updates into a versioned event envelope and enqueue them durably
**FRs covered:** FR5

As the system,
I want to normalize incoming Telegram updates into a single, versioned event envelope and enqueue them durably,
So that downstream processing is replayable and idempotent.

**Acceptance Criteria:**

**Given** the receiver process receives a Telegram update (polling)
**When** the update is accepted
**Then** the system emits exactly one normalized event envelope with fields including `event_id`, `received_at` (UTC), `source`, `telegram_chat_id`, `event_type`, optional `message_id`, `payload` (raw update), and `schema_version`.

**Given** a channel is registered
**When** an envelope is created for an update in that chat
**Then** the envelope includes the internal `channel_id` resolved from `telegram_chat_id`.

**Given** the enqueue operation is retried (at-least-once semantics)
**When** the same update is processed more than once
**Then** the system remains safe to run repeatedly by using idempotency keys (`event_id`) and does not crash or corrupt state.

**Given** structured logging and audit events are enabled
**When** an envelope is enqueued
**Then** a structured log + `audit_events` record is written with `event_type=ingest.enqueued`, `channel_id`, and the `event_id`/correlation id.

### Story 2.2: Consolidate queued envelopes into immutable raw-lake JSONL windows + manifest
**FRs covered:** FR5

As the system,
I want to consolidate queued event envelopes into immutable per-channel JSONL files with a manifest,
So that the system can be rebuilt deterministically from raw inputs.

**Acceptance Criteria:**

**Given** there are queued event envelopes for a registered channel
**When** the consolidator job runs for a fixed time window (e.g., 4 hours)
**Then** it writes an immutable JSONL blob containing those envelopes to the raw lake under a deterministic path that includes `channel_id` and window start/end.

**Given** the JSONL blob is written
**When** the consolidator completes
**Then** it writes a manifest JSON for the same window including `schema_version`, `channel_id`, window boundaries, counts by `event_type`, and a checksum/etag reference.

**Given** the consolidator is re-run for the same window
**When** it encounters an existing blob/manifest for that identity
**Then** it does not overwrite immutable data and instead records a safe no-op (or writes a new versioned location) with an audit event.

### Story 2.3: Process lake window files into “latest message state” with edits and tombstones
**FRs covered:** FR7, FR8, FR9

As the system,
I want to process raw-lake window files into a latest-state message table with “latest wins” semantics,
So that queries operate on correct current message content.

**Acceptance Criteria:**

**Given** a worker processes a lake window file for a channel
**When** it sees `message_new` events
**Then** it upserts a message record keyed by `(channel_id, message_id)` storing message timestamp (UTC) and text/metadata.

**Given** the worker sees message edit events for an existing message
**When** the edit is newer than the stored version
**Then** the stored message text/metadata is updated and marked as the latest version.

**Given** the worker sees a deletion event (when detectable)
**When** it applies that event
**Then** the message is marked as deleted (tombstoned) and excluded from any evidence/citation selection.

### Story 2.4: Implement userbot-based historical backfill and cursoring
**FRs covered:** FR6

As a System Operator,
I want an ops CLI command to backfill historical messages via Telegram Client API and maintain per-channel cursors,
So that the bot can answer from past chat history, not only new messages.

**Acceptance Criteria:**

**Given** the system has userbot credentials configured
**When** the operator runs a backfill command for a registered channel
**Then** the system fetches history using a cursor strategy (e.g., `last_seen_message_id`) and enqueues envelopes with `source=userbot`.

**Given** the backfill runs multiple times
**When** it resumes from a stored cursor
**Then** it does not re-fetch/duplicate work unnecessarily and is safe to retry.

**Given** the backfill completes a page/batch
**When** it advances the cursor
**Then** the cursor is persisted per channel and recorded with an audit event.

### Story 2.5: Ensure retention policy and manual deletion posture are documented and enforced
**FRs covered:** FR10

As a System Operator,
I want the system to retain channel data indefinitely by default and support manual deletion outside the system,
So that the MVP meets retention requirements without complex in-product deletion workflows.

**Acceptance Criteria:**

**Given** messages and derived data are stored
**When** the system runs over time
**Then** it does not automatically purge stored content for MVP.

**Given** a deletion request is received outside the system
**When** the operator follows the documented runbook
**Then** the steps to delete a channel’s stored content (DB + vector + lake if applicable) are clear and repeatable.

## Epic 3: Ask questions in-channel and get evidence-backed answers (Top-3)

Busy Community Member can ask questions (mention/reply), and receive threaded, MarkdownV2 answers with Top-3, citations+dates+cutoff timestamp, contact extraction (no fabrication), conflict-aware formatting, and graceful failure fallback.

### Story 3.1: Detect questions (bot mention / reply-to-bot) and ignore other messages
**FRs covered:** FR11, FR12, FR13

As a Busy Community Member,
I want my question to be recognized when I mention the bot or reply-to-bot,
So that the bot responds only when I’m actually asking it a question.

**Acceptance Criteria:**

**Given** the bot receives a message update in a registered channel
**When** the message is a bot mention
**Then** the system treats it as a question and starts the answer flow.

**Given** the bot receives a message update in a registered channel
**When** the message is a reply to a prior bot message
**Then** the system treats it as a question and starts the answer flow.

**Given** the bot receives a message update in a registered channel
**When** the message is neither a bot mention nor a reply-to-bot
**Then** the system does not treat it as a question and does not respond.

### Story 3.2: Send “typing…” immediately and reply in-thread with a safe fallback on failure
**FRs covered:** FR15, FR44

As a Busy Community Member,
I want immediate feedback that the bot is working and a clear reply even if something fails,
So that the experience feels responsive and reliable.

**Acceptance Criteria:**

**Given** a question is detected
**When** processing begins
**Then** the bot sends a Telegram “typing…” (chat action) promptly.

**Given** the answer flow succeeds
**When** the bot responds
**Then** it replies as a threaded reply to the user’s question message.

**Given** the answer flow fails at any point
**When** the bot responds
**Then** it replies as a threaded reply with: “Sorry, I couldn’t answer right now—please try again later.”

### Story 3.3: Enforce strict channel-scoped retrieval (no cross-channel leakage)
**FRs covered:** (supports the channel isolation requirement)

As a Busy Community Member,
I want answers to only use evidence from the channel I asked in,
So that private information from other channels is not leaked.

**Acceptance Criteria:**

**Given** a question is asked in a channel
**When** the system retrieves candidate evidence
**Then** every retrieval/ranking step applies a mandatory filter for that channel’s `channel_id`.

**Given** there exists similar content in other channels
**When** the system answers
**Then** it does not cite or use evidence outside the current channel.

### Story 3.4: Retrieve, rank, and return Top 3 distinct recommendations with citations and dates
**FRs covered:** FR17, FR18, FR19

As a Busy Community Member,
I want the bot to return the Top 3 most relevant recommendations backed by evidence,
So that I can act quickly with confidence.

**Acceptance Criteria:**

**Given** a question is detected in a registered channel
**When** the system processes it
**Then** it retrieves relevant content for that channel and returns 3 distinct recommendations when applicable.

**Given** a recommendation is presented
**When** the bot formats the answer
**Then** each item includes citations (Telegram message link when possible; fallback citation otherwise) and message dates.

**Given** there are fewer than 3 strong results
**When** the bot responds
**Then** it returns the best available results without fabricating missing recommendations.

### Story 3.5: Always include the cutoff timestamp line (IST) in answers
**FRs covered:** FR20

As a Busy Community Member,
I want every answer to show “as-of” freshness,
So that I understand what time range the bot is based on.

**Acceptance Criteria:**

**Given** the bot sends an answer
**When** formatting the message
**Then** it includes the line “Based on messages up to <cutoff> (IST)” on every answer.

**Given** timestamps are stored internally
**When** they are persisted
**Then** they are stored in UTC and converted to IST only for display.

### Story 3.6: Extract and display contact details only when present in evidence
**FRs covered:** FR21, FR22

As a Busy Community Member,
I want contact details surfaced when they exist in the chat history,
So that I can act without extra searching.

**Acceptance Criteria:**

**Given** evidence messages contain contact details (e.g., phone number)
**When** the bot formats a recommendation
**Then** it includes the extracted contact details.

**Given** evidence messages do not contain contact details
**When** the bot formats a recommendation
**Then** it does not fabricate any contact details and may omit the field.

### Story 3.7: Format answers in Telegram MarkdownV2 safely
**FRs covered:** FR16

As a Busy Community Member,
I want answers to render correctly in Telegram,
So that the content is readable and trustworthy.

**Acceptance Criteria:**

**Given** the bot formats any dynamic content (user query, message excerpts, entity names, disclaimers)
**When** the message is sent
**Then** all dynamic text is escaped using a single shared Telegram MarkdownV2 escape utility.

**Given** formatting errors would break rendering
**When** invalid markdown would otherwise be produced
**Then** the system avoids sending broken markup (escape-first, fail-safe behavior).

### Story 3.8: Handle conflicting recommendations neutrally with evidence
**FRs covered:** FR23

As a Busy Community Member,
I want conflicting opinions to be summarized neutrally with citations,
So that I can decide without reading the whole chat.

**Acceptance Criteria:**

**Given** the evidence indicates disagreement
**When** the bot formats the Top 3 response
**Then** it explicitly notes the disagreement in neutral language
**And** provides citations + dates that support each side.

## Epic 4: Explore more results and enforce per-channel daily quota

Users can page “More recommendations” (+3 up to 12 distinct) without consuming quota; system enforces per-channel daily quota with IST reset and clear refusal messaging when exhausted.

### Story 4.1: Enforce per-channel daily question quota with IST midnight reset
**FRs covered:** FR28, FR29, FR30

As a Busy Community Member,
I want the bot to enforce a daily limit per channel,
So that system usage stays fair and predictable.

**Acceptance Criteria:**

**Given** a channel has a daily quota of 50 questions
**When** a user asks a question that would exceed the quota
**Then** the bot refuses and replies: “Daily quota is over; try again after midnight IST.”

**Given** the current time passes midnight IST
**When** the next question arrives
**Then** the channel’s quota is treated as reset for that day.

### Story 4.2: Provide “More recommendations” button that paginates +3 up to 12 distinct
**FRs covered:** FR24, FR25, FR26, FR27

As a Busy Community Member,
I want to request more recommendations beyond Top 3,
So that I can explore additional options without re-asking.

**Acceptance Criteria:**

**Given** an answer includes Top 3 recommendations
**When** the user clicks “More recommendations”
**Then** the bot returns the next 3 distinct recommendations as a threaded reply/update
**And** this can continue up to 12 distinct total for the same question context.

**Given** “More recommendations” results are returned
**When** they are formatted
**Then** they preserve citations + dates + cutoff timestamp formatting.

**Given** a user clicks “More recommendations”
**When** results are returned
**Then** this does not consume the per-channel daily question quota.

## Epic 5: Safety and feedback loop

System enforces query safety refusal, quarantines unsafe ingested content from normal answering, and captures 👍/👎 feedback events on answers.

### Story 5.1: Query safety gate (refuse flagged queries with a supportive response)
**FRs covered:** FR33

As a Busy Community Member,
I want the bot to refuse unsafe queries appropriately,
So that the product is safe and responsible.

**Acceptance Criteria:**

**Given** a user asks a question
**When** the query safety classifier flags it per policy
**Then** the bot refuses and replies with a supportive safe response
**And** it does not perform retrieval/synthesis for that query.

### Story 5.2: Quarantine unsafe ingested content and hard-filter it from answering
**FRs covered:** FR34

As the system,
I want unsafe ingested content quarantined and excluded from normal retrieval and citations,
So that unsafe content is not amplified.

**Acceptance Criteria:**

**Given** ingested content is classified as quarantinable
**When** it is processed into derived state
**Then** it is marked quarantined with policy metadata.

**Given** a normal user query is processed
**When** evidence is retrieved
**Then** quarantined content is hard-filtered out and never cited.

### Story 5.3: Capture 👍/👎 feedback on bot answers
**FRs covered:** FR31, FR32

As a System Operator,
I want feedback events captured from reactions on bot answers,
So that we can measure helpfulness over time.

**Acceptance Criteria:**

**Given** a bot answer message exists
**When** users react with 👍 or 👎
**Then** the system records a feedback event linked to the answer and channel
**And** records a structured log + `audit_events` record for the feedback.

## Epic 6: Operate and troubleshoot the bot (membership/permissions, audit events, ops messaging)

System detects bot removal/permission changes where available, creates audit events, stops/degrades ingestion appropriately, and provides ops broadcast/per-channel messaging via CLI and internal-only HTTP endpoint.

### Story 6.1: Detect bot removal/permission changes and emit audit events
**FRs covered:** FR35, FR36, FR37, FR38, FR39

As a System Operator,
I want the system to detect bot removal or permission reductions (when Telegram exposes signals),
So that ingestion can be stopped or degraded without noisy failure loops.

**Acceptance Criteria:**

**Given** Telegram provides an update/signal indicating the bot was removed or permissions changed
**When** the system receives the signal
**Then** it records an `audit_events` entry describing the change with channel identifiers.

**Given** the bot is removed from a channel
**When** the system detects it
**Then** it stops (or safely degrades) ingestion attempts for that channel.

### Story 6.2: Ops CLI to send a message to one channel or broadcast to all channels
**FRs covered:** FR40, FR41, FR42

As a System Operator,
I want an ops CLI command to message a specific channel or broadcast to all onboarded channels,
So that I can communicate operationally without a UI.

**Acceptance Criteria:**

**Given** there are registered channels
**When** the operator invokes the CLI to broadcast a message
**Then** the system sends the message to each channel and records an audit event per send (or a batch audit event with per-channel results).

**Given** the operator invokes the CLI to message one channel
**When** the channel exists
**Then** the system sends the message and records an audit event.

### Story 6.3: Internal-only HTTP endpoint for ops messaging
**FRs covered:** FR43

As a System Operator,
I want an internal-only HTTP endpoint to send ops messages,
So that automation can trigger operational messages without exposing a public API.

**Acceptance Criteria:**

**Given** the ops API is network-restricted
**When** an internal request is made to send/broadcast a message
**Then** the system performs the send and returns a structured success response.

**Given** an ops send/broadcast occurs
**When** it completes
**Then** the system records an `audit_events` entry with request id and per-channel results.
