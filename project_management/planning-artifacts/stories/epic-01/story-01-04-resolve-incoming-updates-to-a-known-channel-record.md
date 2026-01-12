---
epic: 1
epic_title: "Onboard a community channel and make the bot usable"
story: "1.4"
story_title: "Resolve incoming updates to a known channel record"
source: "project_management/planning-artifacts/epics.md"
---

# Story 1.4: Resolve incoming updates to a known channel record

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

