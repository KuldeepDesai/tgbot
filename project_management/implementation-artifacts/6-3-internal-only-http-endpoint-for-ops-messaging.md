# Story 6.3: Internal-only HTTP endpoint for ops messaging

Status: done

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As a System Operator,
I want an internal-only HTTP endpoint to send ops messages,
so that automation can trigger operational messages without exposing a public API.

## Acceptance Criteria

1.
   **Given** the ops API is network-restricted
   **When** an internal request is made to send/broadcast a message
   **Then** the system performs the send and returns a structured success response.

2.
   **Given** an ops send/broadcast occurs
   **When** it completes
   **Then** the system records an `audit_events` entry with request id and per-channel results.

## Tasks / Subtasks

- [ ] Implement AC 1: the system performs the send and returns a structured success response. (AC: 1)
  - [ ] Implement core behavior and error handling for this AC
  - [ ] Add/adjust tests covering this AC
- [ ] Implement AC 2: the system records an `audit_events` entry with request id and per-channel results. (AC: 2)
  - [ ] Persist audit event with minimum required fields
  - [ ] Add/adjust tests covering this AC
- [ ] Add regression/quality checks (lint/tests) and update docs if needed (AC: all)
  - [ ] Run the full test suite locally
  - [ ] Confirm no secrets leak into logs

## Dev Notes

- **Sources**:
  - Planning story: `project_management/planning-artifacts/stories/epic-06/story-06-03-internal-only-http-endpoint-for-ops-messaging.md`
  - Epics: `project_management/planning-artifacts/epics.md`
  - Architecture: `project_management/planning-artifacts/architecture.md`
- **Cross-cutting guardrails (from architecture/epics)**:
  - Use `uv` for dependency management; Python async-first; `aiogram==3.24.0`; `Telethon==1.42.0`.
  - Store timestamps in UTC; render IST only at presentation time.
  - Always escape dynamic text for Telegram MarkdownV2 using a single shared utility.
  - Maintain strict channel isolation (`channel_id` scoping) across retrieval/ranking/synthesis.
  - Emit structured logs and audit events with correlation/request IDs where applicable.

### References

- Story key: `6-3-internal-only-http-endpoint-for-ops-messaging`
- `project_management/planning-artifacts/architecture.md` (Starter Template Evaluation; Cross-Cutting Concerns)

## Dev Agent Record

### Agent Model Used

N/A (bulk create-story; model not recorded)

### Debug Log References

### Completion Notes List

### File List

- `src/tgbot/ops/api/app.py`
- `src/tgbot/ops/api/routes/broadcast.py`
- `src/tgbot/main/ops_api.py`
- `src/tgbot/storage/repos/audit_repo.py`
- `src/tgbot/ops/cli/main.py`
- `src/tgbot/storage/repos/messages_repo.py`
- `src/tgbot/worker/file_processor.py`
- `src/tgbot/telegram/handlers/query.py`
- `src/tgbot/telegram/updates/receiver_polling.py`
- `src/tgbot/ingestion/consolidator/consolidate_to_lake.py`
- `migrations/versions/0001_initial_schema.py`
- `src/tgbot/logging/logger.py`
- `src/tgbot/userbot/backfill.py`
- `src/tgbot/storage/models/messages.py`
- `src/tgbot/telegram/handlers/feedback.py`
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

