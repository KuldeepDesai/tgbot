# Story 1.1: Set up initial project from the selected starter template

Status: done

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As a System Operator,
I want the project scaffolded using the approved architecture starter template,
so that the codebase is ready for implementing the bot and pipeline consistently.

## Acceptance Criteria

1.
   **Given** the architecture specifies Python + `uv` + `aiogram` + `Telethon` and a standard directory structure
   **When** the project is initialized
   **Then** the repo contains a Python project scaffold with dependency management in place (via `uv`)
   **And** the bot and pipeline dependencies are added at the pinned versions specified in architecture (or documented equivalents if versions change).

2.
   **Given** the architecture defines standard module boundaries and entrypoints
   **When** the scaffold is created
   **Then** the project contains the expected source layout (e.g., `src/tgbot/...`), migrations skeleton, and runnable entrypoints for receiver/worker/ops.

## Tasks / Subtasks

- [ ] Implement AC 1: the repo contains a Python project scaffold with dependency management in place (via `uv`) (AC: 1)
  - [ ] Implement core behavior and error handling for this AC
  - [ ] Add/adjust tests covering this AC
- [ ] Implement AC 2: the project contains the expected source layout (e.g., `src/tgbot/...`), migrations skeleton, and runnable entrypoints for receiver/worker/ops. (AC: 2)
  - [ ] Implement core behavior and error handling for this AC
  - [ ] Add/adjust tests covering this AC
- [ ] Add regression/quality checks (lint/tests) and update docs if needed (AC: all)
  - [ ] Run the full test suite locally
  - [ ] Confirm no secrets leak into logs

## Dev Notes

- **Sources**:
  - Planning story: `project_management/planning-artifacts/stories/epic-01/story-01-01-set-up-initial-project-from-the-selected-starter-template.md`
  - Epics: `project_management/planning-artifacts/epics.md`
  - Architecture: `project_management/planning-artifacts/architecture.md`
- **Cross-cutting guardrails (from architecture/epics)**:
  - Use `uv` for dependency management; Python async-first; `aiogram==3.24.0`; `Telethon==1.42.0`.
  - Store timestamps in UTC; render IST only at presentation time.
  - Always escape dynamic text for Telegram MarkdownV2 using a single shared utility.
  - Maintain strict channel isolation (`channel_id` scoping) across retrieval/ranking/synthesis.
  - Emit structured logs and audit events with correlation/request IDs where applicable.

### References

- Story key: `1-1-set-up-initial-project-from-the-selected-starter-template`
- `project_management/planning-artifacts/architecture.md` (Starter Template Evaluation; Cross-Cutting Concerns)

## Dev Agent Record

### Agent Model Used

N/A (bulk create-story; model not recorded)

### Debug Log References

### Completion Notes List

### File List

- `pyproject.toml`
- `alembic.ini`
- `migrations/env.py`
- `src/tgbot/main/receiver.py`
- `src/tgbot/main/worker.py`
- `src/tgbot/main/consolidator.py`
- `src/tgbot/main/ops_api.py`
- `src/tgbot/telegram/updates/receiver_polling.py`
- `src/tgbot/userbot/backfill.py`
- `src/tgbot/ops/cli/main.py`
- `migrations/versions/0001_initial_schema.py`
- `src/tgbot/ingestion/consolidator/consolidate_to_lake.py`
- `src/tgbot/storage/repos/channels_repo.py`
- `src/tgbot/ops/api/routes/broadcast.py`
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

