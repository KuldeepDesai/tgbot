---
epic: 2
epic_title: "Capture and maintain the community knowledge base (ingest + backfill + lifecycle)"
story: "2.3"
story_title: "Process lake window files into “latest message state” with edits and tombstones"
source: "project_management/planning-artifacts/epics.md"
---

# Story 2.3: Process lake window files into “latest message state” with edits and tombstones

### Story 2.3: Process lake window files into “latest message state” with edits and tombstones
**FRs covered:** FR7, FR8, FR9

As the system,
I want to process raw-lake window files into a latest-state message table with “latest wins” semantics,
So that queries operate on correct current message content.

**Acceptance Criteria:**

**Given** a worker processes a lake window file for a channel
**When** it sees `message_new` events
**Then** it upserts a message record keyed by `(channel_id, message_id)` storing message timestamp (UTC) and text/metadata.

**Given** the worker sees message edit events for an existing message
**When** the edit is newer than the stored version
**Then** the stored message text/metadata is updated and marked as the latest version.

**Given** the worker sees a deletion event (when detectable)
**When** it applies that event
**Then** the message is marked as deleted (tombstoned) and excluded from any evidence/citation selection.

