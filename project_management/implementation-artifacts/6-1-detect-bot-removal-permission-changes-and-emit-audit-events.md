# Story 6.1: Detect bot removal/permission changes and emit audit events

Status: done

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As a System Operator,
I want the system to detect bot removal or permission reductions (when Telegram exposes signals),
so that ingestion can be stopped or degraded without noisy failure loops.

## Acceptance Criteria

1.
   **Given** Telegram provides an update/signal indicating the bot was removed or permissions changed
   **When** the system receives the signal
   **Then** it records an `audit_events` entry describing the change with channel identifiers.

2.
   **Given** the bot is removed from a channel
   **When** the system detects it
   **Then** it stops (or safely degrades) ingestion attempts for that channel.

## Tasks / Subtasks

- [ ] Implement AC 1: it records an `audit_events` entry describing the change with channel identifiers. (AC: 1)
  - [ ] Persist audit event with minimum required fields
  - [ ] Add/adjust tests covering this AC
- [ ] Implement AC 2: it stops (or safely degrades) ingestion attempts for that channel. (AC: 2)
  - [ ] Implement core behavior and error handling for this AC
  - [ ] Add/adjust tests covering this AC
- [ ] Add regression/quality checks (lint/tests) and update docs if needed (AC: all)
  - [ ] Run the full test suite locally
  - [ ] Confirm no secrets leak into logs

## Dev Notes

- **Sources**:
  - Planning story: `/Users/Kuldeep_Desai/workspace/exp/tgbot/project_management/planning-artifacts/stories/epic-06/story-06-01-detect-bot-removal-permission-changes-and-emit-audit-events.md`
  - Epics: `project_management/planning-artifacts/epics.md`
  - Architecture: `project_management/planning-artifacts/architecture.md`
- **Cross-cutting guardrails (from architecture/epics)**:
  - Use `uv` for dependency management; Python async-first; `aiogram==3.24.0`; `Telethon==1.42.0`.
  - Store timestamps in UTC; render IST only at presentation time.
  - Always escape dynamic text for Telegram MarkdownV2 using a single shared utility.
  - Maintain strict channel isolation (`channel_id` scoping) across retrieval/ranking/synthesis.
  - Emit structured logs and audit events with correlation/request IDs where applicable.

### References

- Story key: `6-1-detect-bot-removal-permission-changes-and-emit-audit-events`
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
