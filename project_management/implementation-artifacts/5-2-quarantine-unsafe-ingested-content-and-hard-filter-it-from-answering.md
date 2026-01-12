# Story 5.2: Quarantine unsafe ingested content and hard-filter it from answering

Status: done

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As a the system,
I want unsafe ingested content quarantined and excluded from normal retrieval and citations,
so that unsafe content is not amplified.

## Acceptance Criteria

1.
   **Given** ingested content is classified as quarantinable
   **When** it is processed into derived state
   **Then** it is marked quarantined with policy metadata.

2.
   **Given** a normal user query is processed
   **When** evidence is retrieved
   **Then** quarantined content is hard-filtered out and never cited.

## Tasks / Subtasks

- [ ] Implement AC 1: it is marked quarantined with policy metadata. (AC: 1)
  - [ ] Implement core behavior and error handling for this AC
  - [ ] Add/adjust tests covering this AC
- [ ] Implement AC 2: quarantined content is hard-filtered out and never cited. (AC: 2)
  - [ ] Implement core behavior and error handling for this AC
  - [ ] Add/adjust tests covering this AC
- [ ] Add regression/quality checks (lint/tests) and update docs if needed (AC: all)
  - [ ] Run the full test suite locally
  - [ ] Confirm no secrets leak into logs

## Dev Notes

- **Sources**:
  - Planning story: `project_management/planning-artifacts/stories/epic-05/story-05-02-quarantine-unsafe-ingested-content-and-hard-filter-it-from-answering.md`
  - Epics: `project_management/planning-artifacts/epics.md`
  - Architecture: `project_management/planning-artifacts/architecture.md`
- **Cross-cutting guardrails (from architecture/epics)**:
  - Use `uv` for dependency management; Python async-first; `aiogram==3.24.0`; `Telethon==1.42.0`.
  - Store timestamps in UTC; render IST only at presentation time.
  - Always escape dynamic text for Telegram MarkdownV2 using a single shared utility.
  - Maintain strict channel isolation (`channel_id` scoping) across retrieval/ranking/synthesis.
  - Emit structured logs and audit events with correlation/request IDs where applicable.

### References

- Story key: `5-2-quarantine-unsafe-ingested-content-and-hard-filter-it-from-answering`
- `project_management/planning-artifacts/architecture.md` (Starter Template Evaluation; Cross-Cutting Concerns)

## Dev Agent Record

### Agent Model Used

N/A (bulk create-story; model not recorded)

### Debug Log References

### Completion Notes List

### File List

- `src/tgbot/safety/message_classifier.py`
- `src/tgbot/query/service.py`
- `src/tgbot/storage/repos/messages_repo.py`
- `src/tgbot/telegram/updates/receiver_polling.py`
- `tests/unit/test_channel_isolation_filters.py`
- `src/tgbot/worker/file_processor.py`
- `src/tgbot/safety/query_gate.py`
- `src/tgbot/telegram/handlers/query.py`
- `src/tgbot/telegram/updates/normalization.py`
- `migrations/env.py`
- `migrations/versions/0001_initial_schema.py`
- `src/tgbot/lake/manifest.py`
- `src/tgbot/storage/models/messages.py`
- `src/tgbot/storage/repos/answers_repo.py`
- `src/tgbot/query/recommendations.py`
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

