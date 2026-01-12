# Story 3.6: Extract and display contact details only when present in evidence

Status: done

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As a Busy Community Member,
I want contact details surfaced when they exist in the chat history,
so that I can act without extra searching.

## Acceptance Criteria

1.
   **Given** evidence messages contain contact details (e.g., phone number)
   **When** the bot formats a recommendation
   **Then** it includes the extracted contact details.

2.
   **Given** evidence messages do not contain contact details
   **When** the bot formats a recommendation
   **Then** it does not fabricate any contact details and may omit the field.

## Tasks / Subtasks

- [ ] Implement AC 1: it includes the extracted contact details. (AC: 1)
  - [ ] Implement core behavior and error handling for this AC
  - [ ] Add/adjust tests covering this AC
- [ ] Implement AC 2: it does not fabricate any contact details and may omit the field. (AC: 2)
  - [ ] Implement core behavior and error handling for this AC
  - [ ] Add/adjust tests covering this AC
- [ ] Add regression/quality checks (lint/tests) and update docs if needed (AC: all)
  - [ ] Run the full test suite locally
  - [ ] Confirm no secrets leak into logs

## Dev Notes

- **Sources**:
  - Planning story: `/Users/Kuldeep_Desai/workspace/exp/tgbot/project_management/planning-artifacts/stories/epic-03/story-03-06-extract-and-display-contact-details-only-when-present-in-evidence.md`
  - Epics: `project_management/planning-artifacts/epics.md`
  - Architecture: `project_management/planning-artifacts/architecture.md`
- **Cross-cutting guardrails (from architecture/epics)**:
  - Use `uv` for dependency management; Python async-first; `aiogram==3.24.0`; `Telethon==1.42.0`.
  - Store timestamps in UTC; render IST only at presentation time.
  - Always escape dynamic text for Telegram MarkdownV2 using a single shared utility.
  - Maintain strict channel isolation (`channel_id` scoping) across retrieval/ranking/synthesis.
  - Emit structured logs and audit events with correlation/request IDs where applicable.

### References

- Story key: `3-6-extract-and-display-contact-details-only-when-present-in-evidence`
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
