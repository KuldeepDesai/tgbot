# Story 2.5: Ensure retention policy and manual deletion posture are documented and enforced

Status: done

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As a System Operator,
I want the system to retain channel data indefinitely by default and support manual deletion outside the system,
so that the MVP meets retention requirements without complex in-product deletion workflows.

## Acceptance Criteria

1.
   **Given** messages and derived data are stored
   **When** the system runs over time
   **Then** it does not automatically purge stored content for MVP.

2.
   **Given** a deletion request is received outside the system
   **When** the operator follows the documented runbook
   **Then** the steps to delete a channel’s stored content (DB + vector + lake if applicable) are clear and repeatable.

## Tasks / Subtasks

- [ ] Implement AC 1: it does not automatically purge stored content for MVP. (AC: 1)
  - [ ] Implement core behavior and error handling for this AC
  - [ ] Add/adjust tests covering this AC
- [ ] Implement AC 2: the steps to delete a channel’s stored content (DB + vector + lake if applicable) are clear and repeatable. (AC: 2)
  - [ ] Implement core behavior and error handling for this AC
  - [ ] Add/adjust tests covering this AC
- [ ] Add regression/quality checks (lint/tests) and update docs if needed (AC: all)
  - [ ] Run the full test suite locally
  - [ ] Confirm no secrets leak into logs

## Dev Notes

- **Sources**:
  - Planning story: `/Users/Kuldeep_Desai/workspace/exp/tgbot/project_management/planning-artifacts/stories/epic-02/story-02-05-ensure-retention-policy-and-manual-deletion-posture-are-documented-and-enforced.md`
  - Epics: `project_management/planning-artifacts/epics.md`
  - Architecture: `project_management/planning-artifacts/architecture.md`
- **Cross-cutting guardrails (from architecture/epics)**:
  - Use `uv` for dependency management; Python async-first; `aiogram==3.24.0`; `Telethon==1.42.0`.
  - Store timestamps in UTC; render IST only at presentation time.
  - Always escape dynamic text for Telegram MarkdownV2 using a single shared utility.
  - Maintain strict channel isolation (`channel_id` scoping) across retrieval/ranking/synthesis.
  - Emit structured logs and audit events with correlation/request IDs where applicable.

### References

- Story key: `2-5-ensure-retention-policy-and-manual-deletion-posture-are-documented-and-enforced`
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
