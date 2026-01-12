# Story 2.4: Implement userbot-based historical backfill and cursoring

Status: done

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As a System Operator,
I want an ops CLI command to backfill historical messages via Telegram Client API and maintain per-channel cursors,
so that the bot can answer from past chat history, not only new messages.

## Acceptance Criteria

1.
   **Given** the system has userbot credentials configured
   **When** the operator runs a backfill command for a registered channel
   **Then** the system fetches history using a cursor strategy (e.g., `last_seen_message_id`) and enqueues envelopes with `source=userbot`.

2.
   **Given** the backfill runs multiple times
   **When** it resumes from a stored cursor
   **Then** it does not re-fetch/duplicate work unnecessarily and is safe to retry.

3.
   **Given** the backfill completes a page/batch
   **When** it advances the cursor
   **Then** the cursor is persisted per channel and recorded with an audit event.

## Tasks / Subtasks

- [ ] Implement AC 1: the system fetches history using a cursor strategy (e.g., `last_seen_message_id`) and enqueues envelopes with `source=userbot`. (AC: 1)
  - [ ] Confirm UTC storage + IST presentation rules are followed
  - [ ] Add/adjust tests covering this AC
- [ ] Implement AC 2: it does not re-fetch/duplicate work unnecessarily and is safe to retry. (AC: 2)
  - [ ] Implement core behavior and error handling for this AC
  - [ ] Add/adjust tests covering this AC
- [ ] Implement AC 3: the cursor is persisted per channel and recorded with an audit event. (AC: 3)
  - [ ] Persist audit event with minimum required fields
  - [ ] Confirm UTC storage + IST presentation rules are followed
  - [ ] Add/adjust tests covering this AC
- [ ] Add regression/quality checks (lint/tests) and update docs if needed (AC: all)
  - [ ] Run the full test suite locally
  - [ ] Confirm no secrets leak into logs

## Dev Notes

- **Sources**:
  - Planning story: `/Users/Kuldeep_Desai/workspace/exp/tgbot/project_management/planning-artifacts/stories/epic-02/story-02-04-implement-userbot-based-historical-backfill-and-cursoring.md`
  - Epics: `project_management/planning-artifacts/epics.md`
  - Architecture: `project_management/planning-artifacts/architecture.md`
- **Cross-cutting guardrails (from architecture/epics)**:
  - Use `uv` for dependency management; Python async-first; `aiogram==3.24.0`; `Telethon==1.42.0`.
  - Store timestamps in UTC; render IST only at presentation time.
  - Always escape dynamic text for Telegram MarkdownV2 using a single shared utility.
  - Maintain strict channel isolation (`channel_id` scoping) across retrieval/ranking/synthesis.
  - Emit structured logs and audit events with correlation/request IDs where applicable.

### References

- Story key: `2-4-implement-userbot-based-historical-backfill-and-cursoring`
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
