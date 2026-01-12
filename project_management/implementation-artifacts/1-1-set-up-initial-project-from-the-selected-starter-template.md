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
  - Planning story: `/Users/Kuldeep_Desai/workspace/exp/tgbot/project_management/planning-artifacts/stories/epic-01/story-01-01-set-up-initial-project-from-the-selected-starter-template.md`
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

{{agent_model_name_version}}

### Debug Log References

### Completion Notes List

### File List

## Change Log

- 2026-01-12: Created implementation story file from planning artifacts (bulk yolo create-story).

## Status

done
