# Story 4.1: Enforce per-channel daily question quota with IST midnight reset

Status: done

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As a Busy Community Member,
I want the bot to enforce a daily limit per channel,
so that system usage stays fair and predictable.

## Acceptance Criteria

1.
   **Given** a channel has a daily quota of 50 questions
   **When** a user asks a question that would exceed the quota
   **Then** the bot refuses and replies: “Daily quota is over; try again after midnight IST.”

2.
   **Given** the current time passes midnight IST
   **When** the next question arrives
   **Then** the channel’s quota is treated as reset for that day.

## Tasks / Subtasks

- [ ] Implement AC 1: the bot refuses and replies: “Daily quota is over; try again after midnight IST.” (AC: 1)
  - [ ] Confirm UTC storage + IST presentation rules are followed
  - [ ] Add/adjust tests covering this AC
- [ ] Implement AC 2: the channel’s quota is treated as reset for that day. (AC: 2)
  - [ ] Confirm UTC storage + IST presentation rules are followed
  - [ ] Add/adjust tests covering this AC
- [ ] Add regression/quality checks (lint/tests) and update docs if needed (AC: all)
  - [ ] Run the full test suite locally
  - [ ] Confirm no secrets leak into logs

## Dev Notes

- **Sources**:
  - Planning story: `/Users/Kuldeep_Desai/workspace/exp/tgbot/project_management/planning-artifacts/stories/epic-04/story-04-01-enforce-per-channel-daily-question-quota-with-ist-midnight-reset.md`
  - Epics: `project_management/planning-artifacts/epics.md`
  - Architecture: `project_management/planning-artifacts/architecture.md`
- **Cross-cutting guardrails (from architecture/epics)**:
  - Use `uv` for dependency management; Python async-first; `aiogram==3.24.0`; `Telethon==1.42.0`.
  - Store timestamps in UTC; render IST only at presentation time.
  - Always escape dynamic text for Telegram MarkdownV2 using a single shared utility.
  - Maintain strict channel isolation (`channel_id` scoping) across retrieval/ranking/synthesis.
  - Emit structured logs and audit events with correlation/request IDs where applicable.

### References

- Story key: `4-1-enforce-per-channel-daily-question-quota-with-ist-midnight-reset`
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
