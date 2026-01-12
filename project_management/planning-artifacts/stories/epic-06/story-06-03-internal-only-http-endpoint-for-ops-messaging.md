---
epic: 6
epic_title: "Operate and troubleshoot the bot (membership/permissions, audit events, ops messaging)"
story: "6.3"
story_title: "Internal-only HTTP endpoint for ops messaging"
source: "project_management/planning-artifacts/epics.md"
---

# Story 6.3: Internal-only HTTP endpoint for ops messaging

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

