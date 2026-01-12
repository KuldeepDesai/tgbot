# Story 3.5: Always include the cutoff timestamp line (IST) in answers

Status: done

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As a Busy Community Member,
I want every answer to show “as-of” freshness,
so that I understand what time range the bot is based on.

## Acceptance Criteria

1.
   **Given** the bot sends an answer
   **When** formatting the message
   **Then** it includes the line “Based on messages up to <cutoff> (IST)” on every answer.

2.
   **Given** timestamps are stored internally
   **When** they are persisted
   **Then** they are stored in UTC and converted to IST only for display.

## Tasks / Subtasks

- [ ] Implement AC 1: it includes the line “Based on messages up to <cutoff> (IST)” on every answer. (AC: 1)
  - [ ] Confirm UTC storage + IST presentation rules are followed
  - [ ] Add/adjust tests covering this AC
- [ ] Implement AC 2: they are stored in UTC and converted to IST only for display. (AC: 2)
  - [ ] Confirm UTC storage + IST presentation rules are followed
  - [ ] Add/adjust tests covering this AC
- [ ] Add regression/quality checks (lint/tests) and update docs if needed (AC: all)
  - [ ] Run the full test suite locally
  - [ ] Confirm no secrets leak into logs

## Dev Notes

- **Sources**:
  - Planning story: `project_management/planning-artifacts/stories/epic-03/story-03-05-always-include-the-cutoff-timestamp-line-ist-in-answers.md`
  - Epics: `project_management/planning-artifacts/epics.md`
  - Architecture: `project_management/planning-artifacts/architecture.md`
- **Cross-cutting guardrails (from architecture/epics)**:
  - Use `uv` for dependency management; Python async-first; `aiogram==3.24.0`; `Telethon==1.42.0`.
  - Store timestamps in UTC; render IST only at presentation time.
  - Always escape dynamic text for Telegram MarkdownV2 using a single shared utility.
  - Maintain strict channel isolation (`channel_id` scoping) across retrieval/ranking/synthesis.
  - Emit structured logs and audit events with correlation/request IDs where applicable.

### References

- Story key: `3-5-always-include-the-cutoff-timestamp-line-ist-in-answers`
- `project_management/planning-artifacts/architecture.md` (Starter Template Evaluation; Cross-Cutting Concerns)

## Dev Agent Record

### Agent Model Used

N/A (bulk create-story; model not recorded)

### Debug Log References

### Completion Notes List

### File List

- `src/tgbot/time/formatters.py`
- `src/tgbot/telegram/ui/answer_format.py`
- `src/tgbot/telegram/handlers/query.py`
- `src/tgbot/storage/repos/answers_repo.py`
- `src/tgbot/storage/repos/messages_repo.py`
- `src/tgbot/query/service.py`
- `migrations/versions/0001_initial_schema.py`
- `src/tgbot/telegram/updates/receiver_polling.py`
- `src/tgbot/storage/models/answers.py`
- `src/tgbot/telegram/handlers/feedback.py`
- `migrations/env.py`
- `src/tgbot/ingestion/consolidator/consolidate_to_lake.py`
- `src/tgbot/safety/message_classifier.py`
- `src/tgbot/storage/models/messages.py`
- `src/tgbot/worker/file_processor.py`
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

