---
epic: 5
epic_title: "Safety and feedback loop"
story: "5.1"
story_title: "Query safety gate (refuse flagged queries with a supportive response)"
source: "project_management/planning-artifacts/epics.md"
---

# Story 5.1: Query safety gate (refuse flagged queries with a supportive response)

### Story 5.1: Query safety gate (refuse flagged queries with a supportive response)
**FRs covered:** FR33

As a Busy Community Member,
I want the bot to refuse unsafe queries appropriately,
So that the product is safe and responsible.

**Acceptance Criteria:**

**Given** a user asks a question
**When** the query safety classifier flags it per policy
**Then** the bot refuses and replies with a supportive safe response
**And** it does not perform retrieval/synthesis for that query.

