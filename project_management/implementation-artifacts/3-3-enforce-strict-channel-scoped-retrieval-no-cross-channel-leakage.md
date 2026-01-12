# Story 3.3: Enforce strict channel-scoped retrieval (no cross-channel leakage)

Status: done

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As a Busy Community Member,
I want answers to only use evidence from the channel I asked in,
so that private information from other channels is not leaked.

## Acceptance Criteria

1.
   **Given** a question is asked in a channel
   **When** the system retrieves candidate evidence
   **Then** every retrieval/ranking step applies a mandatory filter for that channel’s `channel_id`.

2.
   **Given** there exists similar content in other channels
   **When** the system answers
   **Then** it does not cite or use evidence outside the current channel.

## Tasks / Subtasks

- [ ] Implement AC 1: every retrieval/ranking step applies a mandatory filter for that channel’s `channel_id`. (AC: 1)
  - [ ] Implement core behavior and error handling for this AC
  - [ ] Add/adjust tests covering this AC
- [ ] Implement AC 2: it does not cite or use evidence outside the current channel. (AC: 2)
  - [ ] Confirm UTC storage + IST presentation rules are followed
  - [ ] Add/adjust tests covering this AC
- [ ] Add regression/quality checks (lint/tests) and update docs if needed (AC: all)
  - [ ] Run the full test suite locally
  - [ ] Confirm no secrets leak into logs

## Dev Notes

- **Sources**:
  - Planning story: `/Users/Kuldeep_Desai/workspace/exp/tgbot/project_management/planning-artifacts/stories/epic-03/story-03-03-enforce-strict-channel-scoped-retrieval-no-cross-channel-leakage.md`
  - Epics: `project_management/planning-artifacts/epics.md`
  - Architecture: `project_management/planning-artifacts/architecture.md`
- **Cross-cutting guardrails (from architecture/epics)**:
  - Use `uv` for dependency management; Python async-first; `aiogram==3.24.0`; `Telethon==1.42.0`.
  - Store timestamps in UTC; render IST only at presentation time.
  - Always escape dynamic text for Telegram MarkdownV2 using a single shared utility.
  - Maintain strict channel isolation (`channel_id` scoping) across retrieval/ranking/synthesis.
  - Emit structured logs and audit events with correlation/request IDs where applicable.

### References

- Story key: `3-3-enforce-strict-channel-scoped-retrieval-no-cross-channel-leakage`
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
