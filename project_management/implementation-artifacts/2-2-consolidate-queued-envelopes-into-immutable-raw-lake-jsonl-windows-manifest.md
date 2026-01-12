# Story 2.2: Consolidate queued envelopes into immutable raw-lake JSONL windows + manifest

Status: done

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As a the system,
I want to consolidate queued event envelopes into immutable per-channel JSONL files with a manifest,
so that the system can be rebuilt deterministically from raw inputs.

## Acceptance Criteria

1.
   **Given** there are queued event envelopes for a registered channel
   **When** the consolidator job runs for a fixed time window (e.g., 4 hours)
   **Then** it writes an immutable JSONL blob containing those envelopes to the raw lake under a deterministic path that includes `channel_id` and window start/end.

2.
   **Given** the JSONL blob is written
   **When** the consolidator completes
   **Then** it writes a manifest JSON for the same window including `schema_version`, `channel_id`, window boundaries, counts by `event_type`, and a checksum/etag reference.

3.
   **Given** the consolidator is re-run for the same window
   **When** it encounters an existing blob/manifest for that identity
   **Then** it does not overwrite immutable data and instead records a safe no-op (or writes a new versioned location) with an audit event.

## Tasks / Subtasks

- [ ] Implement AC 1: it writes an immutable JSONL blob containing those envelopes to the raw lake under a deterministic path that includes `channel_id` and window start/end. (AC: 1)
  - [ ] Confirm UTC storage + IST presentation rules are followed
  - [ ] Add/adjust tests covering this AC
- [ ] Implement AC 2: it writes a manifest JSON for the same window including `schema_version`, `channel_id`, window boundaries, counts by `event_type`, and a checksum/etag reference. (AC: 2)
  - [ ] Implement core behavior and error handling for this AC
  - [ ] Add/adjust tests covering this AC
- [ ] Implement AC 3: it does not overwrite immutable data and instead records a safe no-op (or writes a new versioned location) with an audit event. (AC: 3)
  - [ ] Persist audit event with minimum required fields
  - [ ] Confirm UTC storage + IST presentation rules are followed
  - [ ] Add/adjust tests covering this AC
- [ ] Add regression/quality checks (lint/tests) and update docs if needed (AC: all)
  - [ ] Run the full test suite locally
  - [ ] Confirm no secrets leak into logs

## Dev Notes

- **Sources**:
  - Planning story: `project_management/planning-artifacts/stories/epic-02/story-02-02-consolidate-queued-envelopes-into-immutable-raw-lake-jsonl-windows-manifest.md`
  - Epics: `project_management/planning-artifacts/epics.md`
  - Architecture: `project_management/planning-artifacts/architecture.md`
- **Cross-cutting guardrails (from architecture/epics)**:
  - Use `uv` for dependency management; Python async-first; `aiogram==3.24.0`; `Telethon==1.42.0`.
  - Store timestamps in UTC; render IST only at presentation time.
  - Always escape dynamic text for Telegram MarkdownV2 using a single shared utility.
  - Maintain strict channel isolation (`channel_id` scoping) across retrieval/ranking/synthesis.
  - Emit structured logs and audit events with correlation/request IDs where applicable.

### References

- Story key: `2-2-consolidate-queued-envelopes-into-immutable-raw-lake-jsonl-windows-manifest`
- `project_management/planning-artifacts/architecture.md` (Starter Template Evaluation; Cross-Cutting Concerns)

## Dev Agent Record

### Agent Model Used

N/A (bulk create-story; model not recorded)

### Debug Log References

### Completion Notes List

### File List

- `src/tgbot/main/consolidator.py`
- `src/tgbot/ingestion/consolidator/consolidate_to_lake.py`
- `src/tgbot/lake/manifest.py`
- `src/tgbot/lake/paths.py`
- `src/tgbot/lake/object_store/factory.py`
- `src/tgbot/worker/file_processor.py`
- `src/tgbot/telegram/updates/receiver_polling.py`
- `src/tgbot/userbot/backfill.py`
- `src/tgbot/ops/cli/main.py`
- `src/tgbot/storage/repos/audit_repo.py`
- `src/tgbot/telegram/handlers/query.py`
- `migrations/versions/0001_initial_schema.py`
- `src/tgbot/logging/logger.py`
- `src/tgbot/lake/reader.py`
- `src/tgbot/storage/models/audit_events.py`
## Change Log

- 2026-01-12: Created implementation story file from planning artifacts (bulk yolo create-story).
- 2026-01-12: Story hygiene pass (normalized planning-story paths, filled agent-model placeholder, removed redundant bottom status block).

## Senior Developer Review (AI)

_Reviewer: AI on 2026-01-12_

### Synthetic File List Basis

- Git diff is empty; the File List below was generated from a deterministic static keyword scan plus known module/story mappings.

### Findings

- **HIGH**: Story is `Status: done` but Tasks/Subtasks are all unchecked; status likely overstates completion and makes audits unreliable.
- **MEDIUM**: No git diff/commit context available; this review is based on static inspection and may miss what actually changed per story.
- **MEDIUM**: Dev Agent Record has no completion notes, debug refs, or rationale tying code to each Acceptance Criterion.

### Outcome

Changes Requested

