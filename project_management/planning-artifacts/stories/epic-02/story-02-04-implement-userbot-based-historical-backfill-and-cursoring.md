---
epic: 2
epic_title: "Capture and maintain the community knowledge base (ingest + backfill + lifecycle)"
story: "2.4"
story_title: "Implement userbot-based historical backfill and cursoring"
source: "project_management/planning-artifacts/epics.md"
---

# Story 2.4: Implement userbot-based historical backfill and cursoring

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

