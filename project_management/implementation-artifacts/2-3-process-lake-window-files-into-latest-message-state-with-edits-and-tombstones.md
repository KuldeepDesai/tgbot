# Story 2.3: Process lake window files into “latest message state” with edits and tombstones

Status: done

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As a the system,
I want to process raw-lake window files into a latest-state message table with “latest wins” semantics,
so that queries operate on correct current message content.

## Acceptance Criteria

1.
   **Given** a worker processes a lake window file for a channel
   **When** it sees `message_new` events
   **Then** it upserts a message record keyed by `(channel_id, message_id)` storing message timestamp (UTC) and text/metadata.

2.
   **Given** the worker sees message edit events for an existing message
   **When** the edit is newer than the stored version
   **Then** the stored message text/metadata is updated and marked as the latest version.

3.
   **Given** the worker sees a deletion event (when detectable)
   **When** it applies that event
   **Then** the message is marked as deleted (tombstoned) and excluded from any evidence/citation selection.

## Tasks / Subtasks

- [ ] Implement AC 1: it upserts a message record keyed by `(channel_id, message_id)` storing message timestamp (UTC) and text/metadata. (AC: 1)
  - [ ] Confirm UTC storage + IST presentation rules are followed
  - [ ] Add/adjust tests covering this AC
- [ ] Implement AC 2: the stored message text/metadata is updated and marked as the latest version. (AC: 2)
  - [ ] Confirm UTC storage + IST presentation rules are followed
  - [ ] Add/adjust tests covering this AC
- [ ] Implement AC 3: the message is marked as deleted (tombstoned) and excluded from any evidence/citation selection. (AC: 3)
  - [ ] Implement core behavior and error handling for this AC
  - [ ] Add/adjust tests covering this AC
- [ ] Add regression/quality checks (lint/tests) and update docs if needed (AC: all)
  - [ ] Run the full test suite locally
  - [ ] Confirm no secrets leak into logs

## Dev Notes

- **Sources**:
  - Planning story: `project_management/planning-artifacts/stories/epic-02/story-02-03-process-lake-window-files-into-latest-message-state-with-edits-and-tombstones.md`
  - Epics: `project_management/planning-artifacts/epics.md`
  - Architecture: `project_management/planning-artifacts/architecture.md`
- **Cross-cutting guardrails (from architecture/epics)**:
  - Use `uv` for dependency management; Python async-first; `aiogram==3.24.0`; `Telethon==1.42.0`.
  - Store timestamps in UTC; render IST only at presentation time.
  - Always escape dynamic text for Telegram MarkdownV2 using a single shared utility.
  - Maintain strict channel isolation (`channel_id` scoping) across retrieval/ranking/synthesis.
  - Emit structured logs and audit events with correlation/request IDs where applicable.

### References

- Story key: `2-3-process-lake-window-files-into-latest-message-state-with-edits-and-tombstones`
- `project_management/planning-artifacts/architecture.md` (Starter Template Evaluation; Cross-Cutting Concerns)

## Dev Agent Record

### Agent Model Used

N/A (bulk create-story; model not recorded)

### Debug Log References

### Completion Notes List

### File List

- `src/tgbot/worker/file_processor.py`
- `src/tgbot/lake/reader.py`
- `src/tgbot/storage/models/messages.py`
- `src/tgbot/storage/repos/messages_repo.py`
- `src/tgbot/ingestion/consolidator/consolidate_to_lake.py`
- `migrations/versions/0001_initial_schema.py`
- `src/tgbot/telegram/updates/receiver_polling.py`
- `src/tgbot/telegram/updates/normalization.py`
- `src/tgbot/lake/manifest.py`
- `src/tgbot/userbot/backfill.py`
- `migrations/env.py`
- `src/tgbot/storage/repos/channels_repo.py`
- `src/tgbot/telegram/handlers/query.py`
- `src/tgbot/main/worker.py`
- `src/tgbot/ops/cli/main.py`
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

