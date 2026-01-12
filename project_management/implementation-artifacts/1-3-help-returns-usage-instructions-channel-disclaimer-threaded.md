# Story 1.3: `/help` returns usage instructions + channel disclaimer (threaded)

Status: done

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As a Busy Community Member,
I want to use `/help` to see how to ask questions and the channel’s disclaimer,
so that I know how to use the bot correctly and safely.

## Acceptance Criteria

1.
   **Given** the bot is running in a registered channel
   **When** a user sends `/help`
   **Then** the bot replies as a threaded reply (reply-to the `/help` message)
   **And** includes usage instructions (how to ask questions)
   **And** includes the per-channel disclaimer text stored for that channel.

2.
   **Given** the bot is running in a channel that is not registered
   **When** a user sends `/help`
   **Then** the bot replies as a threaded reply with a safe, minimal message indicating the channel is not configured
   **And** it does not leak any other channel’s disclaimer.

3.
   **Given** `/help` output contains dynamic text (disclaimer or other values)
   **When** the bot renders the reply
   **Then** all dynamic text is correctly escaped for Telegram MarkdownV2 (no broken formatting).

## Tasks / Subtasks

- [ ] Implement AC 1: the bot replies as a threaded reply (reply-to the `/help` message) (AC: 1)
  - [ ] Confirm UTC storage + IST presentation rules are followed
  - [ ] Add/adjust tests covering this AC
- [ ] Implement AC 2: the bot replies as a threaded reply with a safe, minimal message indicating the channel is not configured (AC: 2)
  - [ ] Confirm UTC storage + IST presentation rules are followed
  - [ ] Add/adjust tests covering this AC
- [ ] Implement AC 3: all dynamic text is correctly escaped for Telegram MarkdownV2 (no broken formatting). (AC: 3)
  - [ ] Ensure Telegram MarkdownV2 escaping for dynamic text
  - [ ] Add/adjust tests covering this AC
- [ ] Add regression/quality checks (lint/tests) and update docs if needed (AC: all)
  - [ ] Run the full test suite locally
  - [ ] Confirm no secrets leak into logs

## Dev Notes

- **Sources**:
  - Planning story: `project_management/planning-artifacts/stories/epic-01/story-01-03-help-returns-usage-instructions-channel-disclaimer-threaded.md`
  - Epics: `project_management/planning-artifacts/epics.md`
  - Architecture: `project_management/planning-artifacts/architecture.md`
- **Cross-cutting guardrails (from architecture/epics)**:
  - Use `uv` for dependency management; Python async-first; `aiogram==3.24.0`; `Telethon==1.42.0`.
  - Store timestamps in UTC; render IST only at presentation time.
  - Always escape dynamic text for Telegram MarkdownV2 using a single shared utility.
  - Maintain strict channel isolation (`channel_id` scoping) across retrieval/ranking/synthesis.
  - Emit structured logs and audit events with correlation/request IDs where applicable.

### References

- Story key: `1-3-help-returns-usage-instructions-channel-disclaimer-threaded`
- `project_management/planning-artifacts/architecture.md` (Starter Template Evaluation; Cross-Cutting Concerns)

## Dev Agent Record

### Agent Model Used

N/A (bulk create-story; model not recorded)

### Debug Log References

### Completion Notes List

### File List

- `src/tgbot/telegram/updates/receiver_polling.py`
- `src/tgbot/telegram/handlers/help.py`
- `src/tgbot/telegram/markdown_v2.py`
- `src/tgbot/storage/repos/channels_repo.py`
- `src/tgbot/ops/cli/main.py`
- `src/tgbot/telegram/handlers/query.py`
- `migrations/versions/0001_initial_schema.py`
- `src/tgbot/ops/api/routes/broadcast.py`
- `src/tgbot/worker/file_processor.py`
- `src/tgbot/storage/repos/answers_repo.py`
- `src/tgbot/storage/repos/messages_repo.py`
- `src/tgbot/userbot/backfill.py`
- `src/tgbot/safety/message_classifier.py`
- `src/tgbot/storage/models/channels.py`
- `src/tgbot/storage/models/messages.py`
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
- **LOW**: `/help` path returns MarkdownV2; ensure every non-escaped fallback string in other handlers is also escaped to avoid broken rendering.

### Outcome

Changes Requested

