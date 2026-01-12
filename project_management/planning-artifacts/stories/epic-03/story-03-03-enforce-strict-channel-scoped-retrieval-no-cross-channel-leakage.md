---
epic: 3
epic_title: "Ask questions in-channel and get evidence-backed answers (Top-3)"
story: "3.3"
story_title: "Enforce strict channel-scoped retrieval (no cross-channel leakage)"
source: "project_management/planning-artifacts/epics.md"
---

# Story 3.3: Enforce strict channel-scoped retrieval (no cross-channel leakage)

### Story 3.3: Enforce strict channel-scoped retrieval (no cross-channel leakage)
**FRs covered:** (supports the channel isolation requirement)

As a Busy Community Member,
I want answers to only use evidence from the channel I asked in,
So that private information from other channels is not leaked.

**Acceptance Criteria:**

**Given** a question is asked in a channel
**When** the system retrieves candidate evidence
**Then** every retrieval/ranking step applies a mandatory filter for that channel’s `channel_id`.

**Given** there exists similar content in other channels
**When** the system answers
**Then** it does not cite or use evidence outside the current channel.

