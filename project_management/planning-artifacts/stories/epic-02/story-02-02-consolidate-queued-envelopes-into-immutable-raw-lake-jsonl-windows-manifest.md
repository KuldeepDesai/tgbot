---
epic: 2
epic_title: "Capture and maintain the community knowledge base (ingest + backfill + lifecycle)"
story: "2.2"
story_title: "Consolidate queued envelopes into immutable raw-lake JSONL windows + manifest"
source: "project_management/planning-artifacts/epics.md"
---

# Story 2.2: Consolidate queued envelopes into immutable raw-lake JSONL windows + manifest

### Story 2.2: Consolidate queued envelopes into immutable raw-lake JSONL windows + manifest
**FRs covered:** FR5

As the system,
I want to consolidate queued event envelopes into immutable per-channel JSONL files with a manifest,
So that the system can be rebuilt deterministically from raw inputs.

**Acceptance Criteria:**

**Given** there are queued event envelopes for a registered channel
**When** the consolidator job runs for a fixed time window (e.g., 4 hours)
**Then** it writes an immutable JSONL blob containing those envelopes to the raw lake under a deterministic path that includes `channel_id` and window start/end.

**Given** the JSONL blob is written
**When** the consolidator completes
**Then** it writes a manifest JSON for the same window including `schema_version`, `channel_id`, window boundaries, counts by `event_type`, and a checksum/etag reference.

**Given** the consolidator is re-run for the same window
**When** it encounters an existing blob/manifest for that identity
**Then** it does not overwrite immutable data and instead records a safe no-op (or writes a new versioned location) with an audit event.

