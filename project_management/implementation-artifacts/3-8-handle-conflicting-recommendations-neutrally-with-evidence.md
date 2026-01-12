# Story 3.8: Handle conflicting recommendations neutrally with evidence

Status: done

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As a Busy Community Member,
I want conflicting opinions to be summarized neutrally with citations,
so that I can decide without reading the whole chat.

## Acceptance Criteria

1.
   **Given** the evidence indicates disagreement
   **When** the bot formats the Top 3 response
   **Then** it explicitly notes the disagreement in neutral language
   **And** provides citations + dates that support each side.

## Tasks / Subtasks

- [ ] Implement AC 1: it explicitly notes the disagreement in neutral language (AC: 1)
  - [ ] Implement core behavior and error handling for this AC
  - [ ] Add/adjust tests covering this AC
- [ ] Add regression/quality checks (lint/tests) and update docs if needed (AC: all)
  - [ ] Run the full test suite locally
  - [ ] Confirm no secrets leak into logs

## Dev Notes

- **Sources**:
  - Planning story: `project_management/planning-artifacts/stories/epic-03/story-03-08-handle-conflicting-recommendations-neutrally-with-evidence.md`
  - Epics: `project_management/planning-artifacts/epics.md`
  - Architecture: `project_management/planning-artifacts/architecture.md`
- **Cross-cutting guardrails (from architecture/epics)**:
  - Use `uv` for dependency management; Python async-first; `aiogram==3.24.0`; `Telethon==1.42.0`.
  - Store timestamps in UTC; render IST only at presentation time.
  - Always escape dynamic text for Telegram MarkdownV2 using a single shared utility.
  - Maintain strict channel isolation (`channel_id` scoping) across retrieval/ranking/synthesis.
  - Emit structured logs and audit events with correlation/request IDs where applicable.

### References

- Story key: `3-8-handle-conflicting-recommendations-neutrally-with-evidence`
- `project_management/planning-artifacts/architecture.md` (Starter Template Evaluation; Cross-Cutting Concerns)

## Dev Agent Record

### Agent Model Used

N/A (bulk create-story; model not recorded)

### Debug Log References

### Completion Notes List

### File List

- `src/tgbot/query/recommendations.py`
- `src/tgbot/telegram/ui/answer_format.py`
- `src/tgbot/telegram/handlers/query.py`
- `src/tgbot/query/service.py`
- `src/tgbot/telegram/updates/receiver_polling.py`
- `src/tgbot/logging/logger.py`
- `tests/unit/test_channel_isolation_filters.py`
- `src/tgbot/storage/models/answers.py`
- `src/tgbot/storage/repos/answers_repo.py`
- `src/tgbot/telegram/handlers/callbacks_more_recs.py`
- `migrations/versions/0001_initial_schema.py`
- `src/tgbot/config/settings.py`
- `src/tgbot/ingestion/queue/local_queue.py`
- `src/tgbot/main/receiver.py`
- `src/tgbot/telegram/ui/keyboards.py`
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

