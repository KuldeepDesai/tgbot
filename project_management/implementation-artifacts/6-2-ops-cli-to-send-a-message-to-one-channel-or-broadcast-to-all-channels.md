# Story 6.2: Ops CLI to send a message to one channel or broadcast to all channels

Status: done

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As a System Operator,
I want an ops CLI command to message a specific channel or broadcast to all onboarded channels,
so that I can communicate operationally without a UI.

## Acceptance Criteria

1.
   **Given** there are registered channels
   **When** the operator invokes the CLI to broadcast a message
   **Then** the system sends the message to each channel and records an audit event per send (or a batch audit event with per-channel results).

2.
   **Given** the operator invokes the CLI to message one channel
   **When** the channel exists
   **Then** the system sends the message and records an audit event.

## Tasks / Subtasks

- [ ] Implement AC 1: the system sends the message to each channel and records an audit event per send (or a batch audit event with per-channel results). (AC: 1)
  - [ ] Persist audit event with minimum required fields
  - [ ] Confirm UTC storage + IST presentation rules are followed
  - [ ] Add/adjust tests covering this AC
- [ ] Implement AC 2: the system sends the message and records an audit event. (AC: 2)
  - [ ] Persist audit event with minimum required fields
  - [ ] Confirm UTC storage + IST presentation rules are followed
  - [ ] Add/adjust tests covering this AC
- [ ] Add regression/quality checks (lint/tests) and update docs if needed (AC: all)
  - [ ] Run the full test suite locally
  - [ ] Confirm no secrets leak into logs

## Dev Notes

- **Sources**:
  - Planning story: `/Users/Kuldeep_Desai/workspace/exp/tgbot/project_management/planning-artifacts/stories/epic-06/story-06-02-ops-cli-to-send-a-message-to-one-channel-or-broadcast-to-all-channels.md`
  - Epics: `project_management/planning-artifacts/epics.md`
  - Architecture: `project_management/planning-artifacts/architecture.md`
- **Cross-cutting guardrails (from architecture/epics)**:
  - Use `uv` for dependency management; Python async-first; `aiogram==3.24.0`; `Telethon==1.42.0`.
  - Store timestamps in UTC; render IST only at presentation time.
  - Always escape dynamic text for Telegram MarkdownV2 using a single shared utility.
  - Maintain strict channel isolation (`channel_id` scoping) across retrieval/ranking/synthesis.
  - Emit structured logs and audit events with correlation/request IDs where applicable.

### References

- Story key: `6-2-ops-cli-to-send-a-message-to-one-channel-or-broadcast-to-all-channels`
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
