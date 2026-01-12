---
epic: 5
epic_title: "Safety and feedback loop"
story: "5.3"
story_title: "Capture 👍/👎 feedback on bot answers"
source: "project_management/planning-artifacts/epics.md"
---

# Story 5.3: Capture 👍/👎 feedback on bot answers

### Story 5.3: Capture 👍/👎 feedback on bot answers
**FRs covered:** FR31, FR32

As a System Operator,
I want feedback events captured from reactions on bot answers,
So that we can measure helpfulness over time.

**Acceptance Criteria:**

**Given** a bot answer message exists
**When** users react with 👍 or 👎
**Then** the system records a feedback event linked to the answer and channel
**And** records a structured log + `audit_events` record for the feedback.

