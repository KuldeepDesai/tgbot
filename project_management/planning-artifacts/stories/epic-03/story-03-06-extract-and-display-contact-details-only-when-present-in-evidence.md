---
epic: 3
epic_title: "Ask questions in-channel and get evidence-backed answers (Top-3)"
story: "3.6"
story_title: "Extract and display contact details only when present in evidence"
source: "project_management/planning-artifacts/epics.md"
---

# Story 3.6: Extract and display contact details only when present in evidence

### Story 3.6: Extract and display contact details only when present in evidence
**FRs covered:** FR21, FR22

As a Busy Community Member,
I want contact details surfaced when they exist in the chat history,
So that I can act without extra searching.

**Acceptance Criteria:**

**Given** evidence messages contain contact details (e.g., phone number)
**When** the bot formats a recommendation
**Then** it includes the extracted contact details.

**Given** evidence messages do not contain contact details
**When** the bot formats a recommendation
**Then** it does not fabricate any contact details and may omit the field.

