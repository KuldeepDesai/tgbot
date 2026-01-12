---
epic: 6
epic_title: "Operate and troubleshoot the bot (membership/permissions, audit events, ops messaging)"
story: "6.2"
story_title: "Ops CLI to send a message to one channel or broadcast to all channels"
source: "project_management/planning-artifacts/epics.md"
---

# Story 6.2: Ops CLI to send a message to one channel or broadcast to all channels

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

