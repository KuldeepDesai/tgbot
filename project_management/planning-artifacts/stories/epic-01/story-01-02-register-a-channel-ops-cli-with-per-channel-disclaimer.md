---
epic: 1
epic_title: "Onboard a community channel and make the bot usable"
story: "1.2"
story_title: "Register a channel (ops CLI) with per-channel disclaimer"
source: "project_management/planning-artifacts/epics.md"
---

# Story 1.2: Register a channel (ops CLI) with per-channel disclaimer

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

