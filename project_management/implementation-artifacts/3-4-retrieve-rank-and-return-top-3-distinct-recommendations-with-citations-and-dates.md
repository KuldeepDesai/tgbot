# Story 3.4: Retrieve, rank, and return Top 3 distinct recommendations with citations and dates

Status: done

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As a Busy Community Member,
I want the bot to return the Top 3 most relevant recommendations backed by evidence,
so that I can act quickly with confidence.

## Acceptance Criteria

1.
   **Given** a question is detected in a registered channel
   **When** the system processes it
   **Then** it retrieves relevant content for that channel and returns 3 distinct recommendations when applicable.

2.
   **Given** multiple evidence messages refer to the same underlying electrician (same provider)
   **When** the system forms the Top 3 list
   **Then** that electrician appears at most once in the results (deduplicated)
   **And** the remaining items (if available) are different electricians.

3.
   **Given** a recommendation is presented
   **When** the bot formats the answer
   **Then** each item includes citations (Telegram message link when possible; fallback citation otherwise) and message dates.

4.
   **Given** there are fewer than 3 strong results
   **When** the bot responds
   **Then** it returns the best available results without fabricating missing recommendations.

## Tasks / Subtasks

- [ ] Implement AC 1: it retrieves relevant content for that channel and returns 3 distinct recommendations when applicable. (AC: 1)
  - [ ] Confirm UTC storage + IST presentation rules are followed
  - [ ] Add/adjust tests covering this AC
- [ ] Implement AC 2: that electrician appears at most once in the results (deduplicated) (AC: 2)
  - [ ] Confirm UTC storage + IST presentation rules are followed
  - [ ] Add/adjust tests covering this AC
- [ ] Implement AC 3: each item includes citations (Telegram message link when possible; fallback citation otherwise) and message dates. (AC: 3)
  - [ ] Implement core behavior and error handling for this AC
  - [ ] Add/adjust tests covering this AC
- [ ] Implement AC 4: it returns the best available results without fabricating missing recommendations. (AC: 4)
  - [ ] Implement core behavior and error handling for this AC
  - [ ] Add/adjust tests covering this AC
- [ ] Add regression/quality checks (lint/tests) and update docs if needed (AC: all)
  - [ ] Run the full test suite locally
  - [ ] Confirm no secrets leak into logs

## Dev Notes

- **Sources**:
  - Planning story: `/Users/Kuldeep_Desai/workspace/exp/tgbot/project_management/planning-artifacts/stories/epic-03/story-03-04-retrieve-rank-and-return-top-3-distinct-recommendations-with-citations-and-dates.md`
  - Epics: `project_management/planning-artifacts/epics.md`
  - Architecture: `project_management/planning-artifacts/architecture.md`
- **Cross-cutting guardrails (from architecture/epics)**:
  - Use `uv` for dependency management; Python async-first; `aiogram==3.24.0`; `Telethon==1.42.0`.
  - Store timestamps in UTC; render IST only at presentation time.
  - Always escape dynamic text for Telegram MarkdownV2 using a single shared utility.
  - Maintain strict channel isolation (`channel_id` scoping) across retrieval/ranking/synthesis.
  - Emit structured logs and audit events with correlation/request IDs where applicable.

### References

- Story key: `3-4-retrieve-rank-and-return-top-3-distinct-recommendations-with-citations-and-dates`
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
