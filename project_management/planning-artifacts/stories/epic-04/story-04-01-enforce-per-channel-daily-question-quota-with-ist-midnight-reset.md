---
epic: 4
epic_title: "Explore more results and enforce per-channel daily quota"
story: "4.1"
story_title: "Enforce per-channel daily question quota with IST midnight reset"
source: "project_management/planning-artifacts/epics.md"
---

# Story 4.1: Enforce per-channel daily question quota with IST midnight reset

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

