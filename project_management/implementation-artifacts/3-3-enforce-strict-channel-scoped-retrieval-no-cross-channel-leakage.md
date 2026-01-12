# Story 3.3: Enforce strict channel-scoped retrieval (no cross-channel leakage)

Status: done

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As a Busy Community Member,
I want answers to only use evidence from the channel I asked in,
so that private information from other channels is not leaked.

## Acceptance Criteria

1.
   **Given** a question is asked in a channel
   **When** the system retrieves candidate evidence
   **Then** every retrieval/ranking step applies a mandatory filter for that channel’s `channel_id`.

2.
   **Given** there exists similar content in other channels
   **When** the system answers
   **Then** it does not cite or use evidence outside the current channel.

## Tasks / Subtasks

- [ ] Implement AC 1: every retrieval/ranking step applies a mandatory filter for that channel’s `channel_id`. (AC: 1)
  - [ ] Implement core behavior and error handling for this AC
  - [ ] Add/adjust tests covering this AC
- [ ] Implement AC 2: it does not cite or use evidence outside the current channel. (AC: 2)
  - [ ] Confirm UTC storage + IST presentation rules are followed
  - [ ] Add/adjust tests covering this AC
- [ ] Add regression/quality checks (lint/tests) and update docs if needed (AC: all)
  - [ ] Run the full test suite locally
  - [ ] Confirm no secrets leak into logs

## Dev Notes

- **Sources**:
  - Planning story: `project_management/planning-artifacts/stories/epic-03/story-03-03-enforce-strict-channel-scoped-retrieval-no-cross-channel-leakage.md`
  - Epics: `project_management/planning-artifacts/epics.md`
  - Architecture: `project_management/planning-artifacts/architecture.md`
- **Cross-cutting guardrails (from architecture/epics)**:
  - Use `uv` for dependency management; Python async-first; `aiogram==3.24.0`; `Telethon==1.42.0`.
  - Store timestamps in UTC; render IST only at presentation time.
  - Always escape dynamic text for Telegram MarkdownV2 using a single shared utility.
  - Maintain strict channel isolation (`channel_id` scoping) across retrieval/ranking/synthesis.
  - Emit structured logs and audit events with correlation/request IDs where applicable.

### References

- Story key: `3-3-enforce-strict-channel-scoped-retrieval-no-cross-channel-leakage`
- `project_management/planning-artifacts/architecture.md` (Starter Template Evaluation; Cross-Cutting Concerns)

## Dev Agent Record

### Agent Model Used

N/A (bulk create-story; model not recorded)

### Debug Log References

### Completion Notes List

### File List

- `src/tgbot/query/service.py`
- `tests/unit/test_channel_isolation_filters.py`
- `src/tgbot/telegram/updates/receiver_polling.py`
- `src/tgbot/telegram/handlers/query.py`
- `migrations/versions/0001_initial_schema.py`
- `src/tgbot/storage/repos/quota_repo.py`
- `src/tgbot/ingestion/consolidator/consolidate_to_lake.py`
- `src/tgbot/lake/manifest.py`
- `src/tgbot/ops/cli/main.py`
- `src/tgbot/storage/repos/channels_repo.py`
- `src/tgbot/telegram/handlers/feedback.py`
- `src/tgbot/ops/api/routes/broadcast.py`
- `src/tgbot/userbot/backfill.py`
- `src/tgbot/storage/models/channel_cursors.py`
- `src/tgbot/storage/repos/messages_repo.py`
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

