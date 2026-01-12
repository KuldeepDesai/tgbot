# Story 3.2: Send “typing…” immediately and reply in-thread with a safe fallback on failure

Status: done

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As a Busy Community Member,
I want immediate feedback that the bot is working and a clear reply even if something fails,
so that the experience feels responsive and reliable.

## Acceptance Criteria

1.
   **Given** a question is detected
   **When** processing begins
   **Then** the bot sends a Telegram “typing…” (chat action) promptly.

2.
   **Given** the answer flow succeeds
   **When** the bot responds
   **Then** it replies as a threaded reply to the user’s question message.

3.
   **Given** the answer flow fails at any point
   **When** the bot responds
   **Then** it replies as a threaded reply with: “Sorry, I couldn’t answer right now—please try again later.”

## Tasks / Subtasks

- [ ] Implement AC 1: the bot sends a Telegram “typing…” (chat action) promptly. (AC: 1)
  - [ ] Implement core behavior and error handling for this AC
  - [ ] Add/adjust tests covering this AC
- [ ] Implement AC 2: it replies as a threaded reply to the user’s question message. (AC: 2)
  - [ ] Implement core behavior and error handling for this AC
  - [ ] Add/adjust tests covering this AC
- [ ] Implement AC 3: it replies as a threaded reply with: “Sorry, I couldn’t answer right now—please try again later.” (AC: 3)
  - [ ] Implement core behavior and error handling for this AC
  - [ ] Add/adjust tests covering this AC
- [ ] Add regression/quality checks (lint/tests) and update docs if needed (AC: all)
  - [ ] Run the full test suite locally
  - [ ] Confirm no secrets leak into logs

## Dev Notes

- **Sources**:
  - Planning story: `/Users/Kuldeep_Desai/workspace/exp/tgbot/project_management/planning-artifacts/stories/epic-03/story-03-02-send-typing-immediately-and-reply-in-thread-with-a-safe-fallback-on-failure.md`
  - Epics: `project_management/planning-artifacts/epics.md`
  - Architecture: `project_management/planning-artifacts/architecture.md`
- **Cross-cutting guardrails (from architecture/epics)**:
  - Use `uv` for dependency management; Python async-first; `aiogram==3.24.0`; `Telethon==1.42.0`.
  - Store timestamps in UTC; render IST only at presentation time.
  - Always escape dynamic text for Telegram MarkdownV2 using a single shared utility.
  - Maintain strict channel isolation (`channel_id` scoping) across retrieval/ranking/synthesis.
  - Emit structured logs and audit events with correlation/request IDs where applicable.

### References

- Story key: `3-2-send-typing-immediately-and-reply-in-thread-with-a-safe-fallback-on-failure`
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
