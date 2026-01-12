# Story 2.1: Normalize Telegram updates into a versioned event envelope and enqueue them durably

Status: done

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As a the system,
I want to normalize incoming Telegram updates into a single, versioned event envelope and enqueue them durably,
so that downstream processing is replayable and idempotent.

## Acceptance Criteria

1.
   **Given** the receiver process receives a Telegram update (polling)
   **When** the update is accepted
   **Then** the system emits exactly one normalized event envelope with fields including `event_id`, `received_at` (UTC), `source`, `telegram_chat_id`, `event_type`, optional `message_id`, `payload` (raw update), and `schema_version`.

2.
   **Given** a channel is registered
   **When** an envelope is created for an update in that chat
   **Then** the envelope includes the internal `channel_id` resolved from `telegram_chat_id`.

3.
   **Given** the enqueue operation is retried (at-least-once semantics)
   **When** the same update is processed more than once
   **Then** the system remains safe to run repeatedly by using idempotency keys (`event_id`) and does not crash or corrupt state.

4.
   **Given** structured logging and audit events are enabled
   **When** an envelope is enqueued
   **Then** a structured log + `audit_events` record is written with `event_type=ingest.enqueued`, `channel_id`, and the `event_id`/correlation id.

## Tasks / Subtasks

- [ ] Implement AC 1: the system emits exactly one normalized event envelope with fields including `event_id`, `received_at` (UTC), `source`, `telegram_chat_id`, `event_type`, optional `message_id`, `payload` (raw update), and `schema_version`. (AC: 1)
  - [ ] Confirm UTC storage + IST presentation rules are followed
  - [ ] Add/adjust tests covering this AC
- [ ] Implement AC 2: the envelope includes the internal `channel_id` resolved from `telegram_chat_id`. (AC: 2)
  - [ ] Confirm UTC storage + IST presentation rules are followed
  - [ ] Add/adjust tests covering this AC
- [ ] Implement AC 3: the system remains safe to run repeatedly by using idempotency keys (`event_id`) and does not crash or corrupt state. (AC: 3)
  - [ ] Make operation idempotent and safe to retry
  - [ ] Add/adjust tests covering this AC
- [ ] Implement AC 4: a structured log + `audit_events` record is written with `event_type=ingest.enqueued`, `channel_id`, and the `event_id`/correlation id. (AC: 4)
  - [ ] Add structured logs with correlation/request id
  - [ ] Persist audit event with minimum required fields
  - [ ] Add/adjust tests covering this AC
- [ ] Add regression/quality checks (lint/tests) and update docs if needed (AC: all)
  - [ ] Run the full test suite locally
  - [ ] Confirm no secrets leak into logs

## Dev Notes

- **Sources**:
  - Planning story: `/Users/Kuldeep_Desai/workspace/exp/tgbot/project_management/planning-artifacts/stories/epic-02/story-02-01-normalize-telegram-updates-into-a-versioned-event-envelope-and-enqueue-them-durably.md`
  - Epics: `project_management/planning-artifacts/epics.md`
  - Architecture: `project_management/planning-artifacts/architecture.md`
- **Cross-cutting guardrails (from architecture/epics)**:
  - Use `uv` for dependency management; Python async-first; `aiogram==3.24.0`; `Telethon==1.42.0`.
  - Store timestamps in UTC; render IST only at presentation time.
  - Always escape dynamic text for Telegram MarkdownV2 using a single shared utility.
  - Maintain strict channel isolation (`channel_id` scoping) across retrieval/ranking/synthesis.
  - Emit structured logs and audit events with correlation/request IDs where applicable.

### References

- Story key: `2-1-normalize-telegram-updates-into-a-versioned-event-envelope-and-enqueue-them-durably`
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
