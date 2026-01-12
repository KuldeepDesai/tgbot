# Story 6.3: Internal-only HTTP endpoint for ops messaging

Status: done

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As a System Operator,
I want an internal-only HTTP endpoint to send ops messages,
so that automation can trigger operational messages without exposing a public API.

## Acceptance Criteria

1.
   **Given** the ops API is network-restricted
   **When** an internal request is made to send/broadcast a message
   **Then** the system performs the send and returns a structured success response.

2.
   **Given** an ops send/broadcast occurs
   **When** it completes
   **Then** the system records an `audit_events` entry with request id and per-channel results.

## Tasks / Subtasks

- [ ] Implement AC 1: the system performs the send and returns a structured success response. (AC: 1)
  - [ ] Implement core behavior and error handling for this AC
  - [ ] Add/adjust tests covering this AC
- [ ] Implement AC 2: the system records an `audit_events` entry with request id and per-channel results. (AC: 2)
  - [ ] Persist audit event with minimum required fields
  - [ ] Add/adjust tests covering this AC
- [ ] Add regression/quality checks (lint/tests) and update docs if needed (AC: all)
  - [ ] Run the full test suite locally
  - [ ] Confirm no secrets leak into logs

## Dev Notes

- **Sources**:
  - Planning story: `/Users/Kuldeep_Desai/workspace/exp/tgbot/project_management/planning-artifacts/stories/epic-06/story-06-03-internal-only-http-endpoint-for-ops-messaging.md`
  - Epics: `project_management/planning-artifacts/epics.md`
  - Architecture: `project_management/planning-artifacts/architecture.md`
- **Cross-cutting guardrails (from architecture/epics)**:
  - Use `uv` for dependency management; Python async-first; `aiogram==3.24.0`; `Telethon==1.42.0`.
  - Store timestamps in UTC; render IST only at presentation time.
  - Always escape dynamic text for Telegram MarkdownV2 using a single shared utility.
  - Maintain strict channel isolation (`channel_id` scoping) across retrieval/ranking/synthesis.
  - Emit structured logs and audit events with correlation/request IDs where applicable.

### References

- Story key: `6-3-internal-only-http-endpoint-for-ops-messaging`
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
