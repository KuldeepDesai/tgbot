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
  - Planning story: `project_management/planning-artifacts/stories/epic-02/story-02-04-implement-userbot-based-historical-backfill-and-cursoring.md`
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

N/A (bulk create-story; model not recorded)

### Debug Log References

### Completion Notes List

### File List

- `src/tgbot/userbot/backfill.py`
- `src/tgbot/userbot/telethon_client.py`
- `src/tgbot/storage/models/channel_cursors.py`
- `src/tgbot/storage/repos/cursors_repo.py`
- `src/tgbot/ops/cli/main.py`
- `src/tgbot/telegram/handlers/query.py`
- `src/tgbot/ingestion/consolidator/consolidate_to_lake.py`
- `src/tgbot/worker/file_processor.py`
- `migrations/versions/0001_initial_schema.py`
- `src/tgbot/telegram/updates/receiver_polling.py`
- `src/tgbot/telegram/updates/normalization.py`
- `src/tgbot/storage/repos/audit_repo.py`
- `migrations/env.py`
- `src/tgbot/telegram/handlers/feedback.py`
- `src/tgbot/ingestion/schema/event_envelope.py`
## Change Log

- 2026-01-12: Created implementation story file from planning artifacts (bulk yolo create-story).
- 2026-01-12: Story hygiene pass (normalized planning-story paths, filled agent-model placeholder, removed redundant bottom status block).

## Senior Developer Review (AI)

_Reviewer: AI on 2026-01-12_

### Synthetic File List Basis

- Git diff is empty; the File List below was generated from a deterministic static keyword scan plus known module/story mappings.

### Findings

- **HIGH**: Story is `Status: done` but Tasks/Subtasks are all unchecked; status likely overstates completion and makes audits unreliable.
- **MEDIUM**: No git diff/commit context available; this review is based on static inspection and may miss what actually changed per story.
- **MEDIUM**: Dev Agent Record has no completion notes, debug refs, or rationale tying code to each Acceptance Criterion.

### Outcome

Changes Requested

