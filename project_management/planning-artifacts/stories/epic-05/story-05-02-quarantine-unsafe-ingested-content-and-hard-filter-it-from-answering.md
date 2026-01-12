---
epic: 5
epic_title: "Safety and feedback loop"
story: "5.2"
story_title: "Quarantine unsafe ingested content and hard-filter it from answering"
source: "project_management/planning-artifacts/epics.md"
---

# Story 5.2: Quarantine unsafe ingested content and hard-filter it from answering

### Story 5.2: Quarantine unsafe ingested content and hard-filter it from answering
**FRs covered:** FR34

As the system,
I want unsafe ingested content quarantined and excluded from normal retrieval and citations,
So that unsafe content is not amplified.

**Acceptance Criteria:**

**Given** ingested content is classified as quarantinable
**When** it is processed into derived state
**Then** it is marked quarantined with policy metadata.

**Given** a normal user query is processed
**When** evidence is retrieved
**Then** quarantined content is hard-filtered out and never cited.

