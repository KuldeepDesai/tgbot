# Story 1.5: Create minimal persistence for channels and audit events

Status: done

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As a System Operator,
I want onboarding and audit events to be persisted in Postgres,
so that configuration and operational actions are durable and inspectable.

## Acceptance Criteria

1.
   **Given** the project has a migrations mechanism
   **When** migrations are applied to a new database
   **Then** the database has a `channels` table that can store (at minimum) `id` (internal `channel_id`), `telegram_chat_id` (unique), `disclaimer_text`, and timestamps
   **And** the database has an `audit_events` table that can store (at minimum) `id`, `event_type`, `event_ts`, optional `channel_id`, `correlation_id`, and `payload_json`.

2.
   **Given** the `channels` table exists
   **When** Story 1.1’s ops command upserts a channel
   **Then** the data is persisted and readable on subsequent runs/restarts.

3.
   **Given** the `audit_events` table exists
   **When** Story 1.1 or Story 1.3 records an audit event
   **Then** the audit event is persisted and queryable by `event_type` and time range.

## Tasks / Subtasks

- [ ] Implement AC 1: the database has a `channels` table that can store (at minimum) `id` (internal `channel_id`), `telegram_chat_id` (unique), `disclaimer_text`, and timestamps (AC: 1)
  - [ ] Persist audit event with minimum required fields
  - [ ] Add/adjust tests covering this AC
- [ ] Implement AC 2: the data is persisted and readable on subsequent runs/restarts. (AC: 2)
  - [ ] Confirm UTC storage + IST presentation rules are followed
  - [ ] Add/adjust tests covering this AC
- [ ] Implement AC 3: the audit event is persisted and queryable by `event_type` and time range. (AC: 3)
  - [ ] Persist audit event with minimum required fields
  - [ ] Confirm UTC storage + IST presentation rules are followed
  - [ ] Add/adjust tests covering this AC
- [ ] Add regression/quality checks (lint/tests) and update docs if needed (AC: all)
  - [ ] Run the full test suite locally
  - [ ] Confirm no secrets leak into logs

## Dev Notes

- **Sources**:
  - Planning story: `/Users/Kuldeep_Desai/workspace/exp/tgbot/project_management/planning-artifacts/stories/epic-01/story-01-05-create-minimal-persistence-for-channels-and-audit-events.md`
  - Epics: `project_management/planning-artifacts/epics.md`
  - Architecture: `project_management/planning-artifacts/architecture.md`
- **Cross-cutting guardrails (from architecture/epics)**:
  - Use `uv` for dependency management; Python async-first; `aiogram==3.24.0`; `Telethon==1.42.0`.
  - Store timestamps in UTC; render IST only at presentation time.
  - Always escape dynamic text for Telegram MarkdownV2 using a single shared utility.
  - Maintain strict channel isolation (`channel_id` scoping) across retrieval/ranking/synthesis.
  - Emit structured logs and audit events with correlation/request IDs where applicable.

### References

- Story key: `1-5-create-minimal-persistence-for-channels-and-audit-events`
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
