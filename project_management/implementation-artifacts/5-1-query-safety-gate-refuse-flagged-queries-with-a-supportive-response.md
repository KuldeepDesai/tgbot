# Story 5.1: Query safety gate (refuse flagged queries with a supportive response)

Status: done

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As a Busy Community Member,
I want the bot to refuse unsafe queries appropriately,
so that the product is safe and responsible.

## Acceptance Criteria

1.
   **Given** a user asks a question
   **When** the query safety classifier flags it per policy
   **Then** the bot refuses and replies with a supportive safe response
   **And** it does not perform retrieval/synthesis for that query.

## Tasks / Subtasks

- [ ] Implement AC 1: the bot refuses and replies with a supportive safe response (AC: 1)
  - [ ] Implement core behavior and error handling for this AC
  - [ ] Add/adjust tests covering this AC
- [ ] Add regression/quality checks (lint/tests) and update docs if needed (AC: all)
  - [ ] Run the full test suite locally
  - [ ] Confirm no secrets leak into logs

## Dev Notes

- **Sources**:
  - Planning story: `project_management/planning-artifacts/stories/epic-05/story-05-01-query-safety-gate-refuse-flagged-queries-with-a-supportive-response.md`
  - Epics: `project_management/planning-artifacts/epics.md`
  - Architecture: `project_management/planning-artifacts/architecture.md`
- **Cross-cutting guardrails (from architecture/epics)**:
  - Use `uv` for dependency management; Python async-first; `aiogram==3.24.0`; `Telethon==1.42.0`.
  - Store timestamps in UTC; render IST only at presentation time.
  - Always escape dynamic text for Telegram MarkdownV2 using a single shared utility.
  - Maintain strict channel isolation (`channel_id` scoping) across retrieval/ranking/synthesis.
  - Emit structured logs and audit events with correlation/request IDs where applicable.

### References

- Story key: `5-1-query-safety-gate-refuse-flagged-queries-with-a-supportive-response`
- `project_management/planning-artifacts/architecture.md` (Starter Template Evaluation; Cross-Cutting Concerns)

## Dev Agent Record

### Agent Model Used

N/A (bulk create-story; model not recorded)

### Debug Log References

### Completion Notes List

### File List

- `src/tgbot/safety/query_gate.py`
- `src/tgbot/telegram/handlers/query.py`
- `src/tgbot/safety/message_classifier.py`
- `src/tgbot/telegram/updates/receiver_polling.py`
- `src/tgbot/config/settings.py`
- `src/tgbot/query/service.py`
- `src/tgbot/storage/repos/quota_repo.py`
- `src/tgbot/storage/repos/answers_repo.py`
- `src/tgbot/worker/file_processor.py`
- `tests/unit/test_channel_isolation_filters.py`
- `migrations/versions/0001_initial_schema.py`
- `src/tgbot/storage/repos/messages_repo.py`
- `src/tgbot/telegram/handlers/help.py`
- `src/tgbot/telegram/ui/answer_format.py`
- `src/tgbot/ingestion/queue/local_queue.py`
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

