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
  - Planning story: `/Users/Kuldeep_Desai/workspace/exp/tgbot/project_management/planning-artifacts/stories/epic-03/story-03-07-format-answers-in-telegram-markdownv2-safely.md`
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

{{agent_model_name_version}}

### Debug Log References

### Completion Notes List

### File List

## Change Log

- 2026-01-12: Created implementation story file from planning artifacts (bulk yolo create-story).

## Status

done
