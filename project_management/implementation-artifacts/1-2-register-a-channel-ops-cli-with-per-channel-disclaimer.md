# Story 1.2: Register a channel (ops CLI) with per-channel disclaimer

Status: done

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As a System Operator,
I want to register a Telegram channel (by `telegram_chat_id`) and set/update its disclaimer,
so that the bot can recognize the channel and show the correct disclaimer.

## Acceptance Criteria

1.
   **Given** I have access to the ops CLI and Postgres is reachable
   **When** I run a command to register a channel with `telegram_chat_id` and `disclaimer_text`
   **Then** the system creates a `channels` record (or updates the existing one) keyed by `telegram_chat_id`
   **And** the command returns the saved channel identity (including internal `channel_id`) and a success status.

2.
   **Given** a channel is already registered
   **When** I re-run the register command with the same `telegram_chat_id` and a new `disclaimer_text`
   **Then** the system updates the stored disclaimer for that channel (idempotent upsert)
   **And** the operator is informed that changes are effective after app restart (MVP behavior).

3.
   **Given** the operator passes invalid inputs (missing/empty disclaimer, invalid chat id format)
   **When** the command runs
   **Then** it fails with a clear validation error
   **And** it does not create or modify any channel record.

4.
   **Given** structured logging is enabled
   **When** a channel is created or updated
   **Then** the system emits a structured log including `channel_id`, `telegram_chat_id`, action (`created`/`updated`), and a correlation/request id.

5.
   **Given** the system persists audit events to Postgres
   **When** a channel is created or updated via the ops CLI
   **Then** an `audit_events` record is written containing at least `event_type`, `event_ts`, `channel_id`, correlation/request id, and a small `payload_json` including `telegram_chat_id` and action (`created`/`updated`).

## Tasks / Subtasks

- [ ] Implement AC 1: the system creates a `channels` record (or updates the existing one) keyed by `telegram_chat_id` (AC: 1)
  - [ ] Confirm UTC storage + IST presentation rules are followed
  - [ ] Add/adjust tests covering this AC
- [ ] Implement AC 2: the system updates the stored disclaimer for that channel (idempotent upsert) (AC: 2)
  - [ ] Make operation idempotent and safe to retry
  - [ ] Confirm UTC storage + IST presentation rules are followed
  - [ ] Add/adjust tests covering this AC
- [ ] Implement AC 3: it fails with a clear validation error (AC: 3)
  - [ ] Implement core behavior and error handling for this AC
  - [ ] Add/adjust tests covering this AC
- [ ] Implement AC 4: the system emits a structured log including `channel_id`, `telegram_chat_id`, action (`created`/`updated`), and a correlation/request id. (AC: 4)
  - [ ] Add structured logs with correlation/request id
  - [ ] Add/adjust tests covering this AC
- [ ] Implement AC 5: an `audit_events` record is written containing at least `event_type`, `event_ts`, `channel_id`, correlation/request id, and a small `payload_json` including `telegram_chat_id` and action (`created`/`updated`). (AC: 5)
  - [ ] Persist audit event with minimum required fields
  - [ ] Confirm UTC storage + IST presentation rules are followed
  - [ ] Add/adjust tests covering this AC
- [ ] Add regression/quality checks (lint/tests) and update docs if needed (AC: all)
  - [ ] Run the full test suite locally
  - [ ] Confirm no secrets leak into logs

## Dev Notes

- **Sources**:
  - Planning story: `/Users/Kuldeep_Desai/workspace/exp/tgbot/project_management/planning-artifacts/stories/epic-01/story-01-02-register-a-channel-ops-cli-with-per-channel-disclaimer.md`
  - Epics: `project_management/planning-artifacts/epics.md`
  - Architecture: `project_management/planning-artifacts/architecture.md`
- **Cross-cutting guardrails (from architecture/epics)**:
  - Use `uv` for dependency management; Python async-first; `aiogram==3.24.0`; `Telethon==1.42.0`.
  - Store timestamps in UTC; render IST only at presentation time.
  - Always escape dynamic text for Telegram MarkdownV2 using a single shared utility.
  - Maintain strict channel isolation (`channel_id` scoping) across retrieval/ranking/synthesis.
  - Emit structured logs and audit events with correlation/request IDs where applicable.

### References

- Story key: `1-2-register-a-channel-ops-cli-with-per-channel-disclaimer`
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
