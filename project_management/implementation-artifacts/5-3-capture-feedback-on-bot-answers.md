# Story 5.3: Capture 👍/👎 feedback on bot answers

Status: done

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As a System Operator,
I want feedback events captured from reactions on bot answers,
so that we can measure helpfulness over time.

## Acceptance Criteria

1.
   **Given** a bot answer message exists
   **When** users react with 👍 or 👎
   **Then** the system records a feedback event linked to the answer and channel
   **And** records a structured log + `audit_events` record for the feedback.

## Tasks / Subtasks

- [ ] Implement AC 1: the system records a feedback event linked to the answer and channel (AC: 1)
  - [ ] Add structured logs with correlation/request id
  - [ ] Persist audit event with minimum required fields
  - [ ] Confirm UTC storage + IST presentation rules are followed
  - [ ] Add/adjust tests covering this AC
- [ ] Add regression/quality checks (lint/tests) and update docs if needed (AC: all)
  - [ ] Run the full test suite locally
  - [ ] Confirm no secrets leak into logs

## Dev Notes

- **Sources**:
  - Planning story: `/Users/Kuldeep_Desai/workspace/exp/tgbot/project_management/planning-artifacts/stories/epic-05/story-05-03-capture-feedback-on-bot-answers.md`
  - Epics: `project_management/planning-artifacts/epics.md`
  - Architecture: `project_management/planning-artifacts/architecture.md`
- **Cross-cutting guardrails (from architecture/epics)**:
  - Use `uv` for dependency management; Python async-first; `aiogram==3.24.0`; `Telethon==1.42.0`.
  - Store timestamps in UTC; render IST only at presentation time.
  - Always escape dynamic text for Telegram MarkdownV2 using a single shared utility.
  - Maintain strict channel isolation (`channel_id` scoping) across retrieval/ranking/synthesis.
  - Emit structured logs and audit events with correlation/request IDs where applicable.

### References

- Story key: `5-3-capture-feedback-on-bot-answers`
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
