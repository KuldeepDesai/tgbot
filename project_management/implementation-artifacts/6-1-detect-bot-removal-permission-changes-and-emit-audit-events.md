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
  - Planning story: `project_management/planning-artifacts/stories/epic-06/story-06-01-detect-bot-removal-permission-changes-and-emit-audit-events.md`
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

N/A (bulk create-story; model not recorded)

### Debug Log References

### Completion Notes List

### File List

- `src/tgbot/telegram/updates/receiver_polling.py`
- `src/tgbot/storage/repos/audit_repo.py`
- `migrations/versions/0001_initial_schema.py`
- `src/tgbot/worker/file_processor.py`
- `src/tgbot/storage/repos/channels_repo.py`
- `src/tgbot/ops/cli/main.py`
- `src/tgbot/userbot/backfill.py`
- `src/tgbot/ops/api/routes/broadcast.py`
- `src/tgbot/storage/models/audit_events.py`
- `src/tgbot/telegram/handlers/query.py`
- `src/tgbot/telegram/updates/normalization.py`
- `src/tgbot/ingestion/consolidator/consolidate_to_lake.py`
- `src/tgbot/telegram/handlers/feedback.py`
- `src/tgbot/storage/models/channels.py`
- `migrations/env.py`
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

