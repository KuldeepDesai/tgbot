# Story 3.1: Detect questions (bot mention / reply-to-bot) and ignore other messages

Status: done

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As a Busy Community Member,
I want my question to be recognized when I mention the bot or reply-to-bot,
so that the bot responds only when I’m actually asking it a question.

## Acceptance Criteria

1.
   **Given** the bot receives a message update in a registered channel
   **When** the message is a bot mention
   **Then** the system treats it as a question and starts the answer flow.

2.
   **Given** the bot receives a message update in a registered channel
   **When** the message is a reply to a prior bot message
   **Then** the system treats it as a question and starts the answer flow.

3.
   **Given** the bot receives a message update in a registered channel
   **When** the message is neither a bot mention nor a reply-to-bot
   **Then** the system does not treat it as a question and does not respond.

## Tasks / Subtasks

- [ ] Implement AC 1: the system treats it as a question and starts the answer flow. (AC: 1)
  - [ ] Confirm UTC storage + IST presentation rules are followed
  - [ ] Add/adjust tests covering this AC
- [ ] Implement AC 2: the system treats it as a question and starts the answer flow. (AC: 2)
  - [ ] Confirm UTC storage + IST presentation rules are followed
  - [ ] Add/adjust tests covering this AC
- [ ] Implement AC 3: the system does not treat it as a question and does not respond. (AC: 3)
  - [ ] Confirm UTC storage + IST presentation rules are followed
  - [ ] Add/adjust tests covering this AC
- [ ] Add regression/quality checks (lint/tests) and update docs if needed (AC: all)
  - [ ] Run the full test suite locally
  - [ ] Confirm no secrets leak into logs

## Dev Notes

- **Sources**:
  - Planning story: `project_management/planning-artifacts/stories/epic-03/story-03-01-detect-questions-bot-mention-reply-to-bot-and-ignore-other-messages.md`
  - Epics: `project_management/planning-artifacts/epics.md`
  - Architecture: `project_management/planning-artifacts/architecture.md`
- **Cross-cutting guardrails (from architecture/epics)**:
  - Use `uv` for dependency management; Python async-first; `aiogram==3.24.0`; `Telethon==1.42.0`.
  - Store timestamps in UTC; render IST only at presentation time.
  - Always escape dynamic text for Telegram MarkdownV2 using a single shared utility.
  - Maintain strict channel isolation (`channel_id` scoping) across retrieval/ranking/synthesis.
  - Emit structured logs and audit events with correlation/request IDs where applicable.

### References

- Story key: `3-1-detect-questions-bot-mention-reply-to-bot-and-ignore-other-messages`
- `project_management/planning-artifacts/architecture.md` (Starter Template Evaluation; Cross-Cutting Concerns)

## Dev Agent Record

### Agent Model Used

N/A (bulk create-story; model not recorded)

### Debug Log References

### Completion Notes List

### File List

- `src/tgbot/telegram/updates/receiver_polling.py`
- `src/tgbot/telegram/handlers/query.py`
- `migrations/versions/0001_initial_schema.py`
- `src/tgbot/storage/repos/messages_repo.py`
- `src/tgbot/worker/file_processor.py`
- `src/tgbot/storage/models/messages.py`
- `src/tgbot/storage/repos/answers_repo.py`
- `src/tgbot/ingestion/consolidator/consolidate_to_lake.py`
- `src/tgbot/query/service.py`
- `src/tgbot/storage/repos/quota_repo.py`
- `src/tgbot/telegram/handlers/feedback.py`
- `src/tgbot/telegram/updates/normalization.py`
- `src/tgbot/userbot/backfill.py`
- `tests/unit/test_channel_isolation_filters.py`
- `src/tgbot/safety/message_classifier.py`
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

