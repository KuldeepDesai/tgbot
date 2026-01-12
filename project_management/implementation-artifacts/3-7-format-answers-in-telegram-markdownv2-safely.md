# Story 3.7: Format answers in Telegram MarkdownV2 safely

Status: done

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As a Busy Community Member,
I want answers to render correctly in Telegram,
so that the content is readable and trustworthy.

## Acceptance Criteria

1.
   **Given** the bot formats any dynamic content (user query, message excerpts, entity names, disclaimers)
   **When** the message is sent
   **Then** all dynamic text is escaped using a single shared Telegram MarkdownV2 escape utility.

2.
   **Given** formatting errors would break rendering
   **When** invalid markdown would otherwise be produced
   **Then** the system avoids sending broken markup (escape-first, fail-safe behavior).

## Tasks / Subtasks

- [ ] Implement AC 1: all dynamic text is escaped using a single shared Telegram MarkdownV2 escape utility. (AC: 1)
  - [ ] Ensure Telegram MarkdownV2 escaping for dynamic text
  - [ ] Add/adjust tests covering this AC
- [ ] Implement AC 2: the system avoids sending broken markup (escape-first, fail-safe behavior). (AC: 2)
  - [ ] Ensure Telegram MarkdownV2 escaping for dynamic text
  - [ ] Add/adjust tests covering this AC
- [ ] Add regression/quality checks (lint/tests) and update docs if needed (AC: all)
  - [ ] Run the full test suite locally
  - [ ] Confirm no secrets leak into logs

## Dev Notes

- **Sources**:
  - Planning story: `project_management/planning-artifacts/stories/epic-03/story-03-07-format-answers-in-telegram-markdownv2-safely.md`
  - Epics: `project_management/planning-artifacts/epics.md`
  - Architecture: `project_management/planning-artifacts/architecture.md`
- **Cross-cutting guardrails (from architecture/epics)**:
  - Use `uv` for dependency management; Python async-first; `aiogram==3.24.0`; `Telethon==1.42.0`.
  - Store timestamps in UTC; render IST only at presentation time.
  - Always escape dynamic text for Telegram MarkdownV2 using a single shared utility.
  - Maintain strict channel isolation (`channel_id` scoping) across retrieval/ranking/synthesis.
  - Emit structured logs and audit events with correlation/request IDs where applicable.

### References

- Story key: `3-7-format-answers-in-telegram-markdownv2-safely`
- `project_management/planning-artifacts/architecture.md` (Starter Template Evaluation; Cross-Cutting Concerns)

## Dev Agent Record

### Agent Model Used

N/A (bulk create-story; model not recorded)

### Debug Log References

### Completion Notes List

### File List

- `src/tgbot/telegram/markdown_v2.py`
- `tests/unit/test_markdown_v2.py`
- `src/tgbot/telegram/handlers/query.py`
- `src/tgbot/telegram/updates/receiver_polling.py`
- `src/tgbot/telegram/ui/answer_format.py`
- `src/tgbot/storage/repos/answers_repo.py`
- `src/tgbot/ops/cli/main.py`
- `migrations/versions/0001_initial_schema.py`
- `src/tgbot/telegram/handlers/help.py`
- `src/tgbot/safety/query_gate.py`
- `src/tgbot/ops/api/routes/broadcast.py`
- `src/tgbot/safety/message_classifier.py`
- `src/tgbot/storage/repos/messages_repo.py`
- `src/tgbot/worker/file_processor.py`
- `src/tgbot/query/recommendations.py`
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

