---
epic: 3
epic_title: "Ask questions in-channel and get evidence-backed answers (Top-3)"
story: "3.5"
story_title: "Always include the cutoff timestamp line (IST) in answers"
source: "project_management/planning-artifacts/epics.md"
---

# Story 3.5: Always include the cutoff timestamp line (IST) in answers

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

