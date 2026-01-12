---
epic: 1
epic_title: "Onboard a community channel and make the bot usable"
story: "1.5"
story_title: "Create minimal persistence for channels and audit events"
source: "project_management/planning-artifacts/epics.md"
---

# Story 1.5: Create minimal persistence for channels and audit events

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

