# Story 1.4: Resolve incoming updates to a known channel record

Status: done

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As a the system,
I want to associate every incoming Telegram update to a known channel record (or ignore/log unknown channels),
so that multi-channel operation works reliably and safely.

## Acceptance Criteria

1.
   **Given** the receiver gets a Telegram update containing a `chat_id`
   **When** the system looks up the channel by `telegram_chat_id`
   **Then** it resolves the internal `channel_id` and attaches it to downstream processing for that update.

2.
   **Given** the receiver gets an update for an unregistered `chat_id`
   **When** the system processes it
   **Then** it does not ingest/process/store the message as normal content
   **And** it records a structured log + `audit_events` entry indicating “unknown channel” with the `telegram_chat_id`
   **And** it does not respond in-channel (silent by default for MVP).

## Tasks / Subtasks

- [ ] Implement AC 1: it resolves the internal `channel_id` and attaches it to downstream processing for that update. (AC: 1)
  - [ ] Implement core behavior and error handling for this AC
  - [ ] Add/adjust tests covering this AC
- [ ] Implement AC 2: it does not ingest/process/store the message as normal content (AC: 2)
  - [ ] Add structured logs with correlation/request id
  - [ ] Persist audit event with minimum required fields
  - [ ] Confirm UTC storage + IST presentation rules are followed
  - [ ] Add/adjust tests covering this AC
- [ ] Add regression/quality checks (lint/tests) and update docs if needed (AC: all)
  - [ ] Run the full test suite locally
  - [ ] Confirm no secrets leak into logs

## Dev Notes

- **Sources**:
  - Planning story: `/Users/Kuldeep_Desai/workspace/exp/tgbot/project_management/planning-artifacts/stories/epic-01/story-01-04-resolve-incoming-updates-to-a-known-channel-record.md`
  - Epics: `project_management/planning-artifacts/epics.md`
  - Architecture: `project_management/planning-artifacts/architecture.md`
- **Cross-cutting guardrails (from architecture/epics)**:
  - Use `uv` for dependency management; Python async-first; `aiogram==3.24.0`; `Telethon==1.42.0`.
  - Store timestamps in UTC; render IST only at presentation time.
  - Always escape dynamic text for Telegram MarkdownV2 using a single shared utility.
  - Maintain strict channel isolation (`channel_id` scoping) across retrieval/ranking/synthesis.
  - Emit structured logs and audit events with correlation/request IDs where applicable.

### References

- Story key: `1-4-resolve-incoming-updates-to-a-known-channel-record`
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
