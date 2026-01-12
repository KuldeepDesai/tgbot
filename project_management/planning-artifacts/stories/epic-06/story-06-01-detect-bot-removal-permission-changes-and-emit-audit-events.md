---
epic: 6
epic_title: "Operate and troubleshoot the bot (membership/permissions, audit events, ops messaging)"
story: "6.1"
story_title: "Detect bot removal/permission changes and emit audit events"
source: "project_management/planning-artifacts/epics.md"
---

# Story 6.1: Detect bot removal/permission changes and emit audit events

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

