---
epic: 2
epic_title: "Capture and maintain the community knowledge base (ingest + backfill + lifecycle)"
story: "2.1"
story_title: "Normalize Telegram updates into a versioned event envelope and enqueue them durably"
source: "project_management/planning-artifacts/epics.md"
---

# Story 2.1: Normalize Telegram updates into a versioned event envelope and enqueue them durably

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

