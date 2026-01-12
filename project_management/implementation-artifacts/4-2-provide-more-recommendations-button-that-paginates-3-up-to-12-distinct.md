# Story 4.2: Provide “More recommendations” button that paginates +3 up to 12 distinct

Status: done

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As a Busy Community Member,
I want to request more recommendations beyond Top 3,
so that I can explore additional options without re-asking.

## Acceptance Criteria

1.
   **Given** an answer includes Top 3 recommendations
   **When** the user clicks “More recommendations”
   **Then** the bot returns the next 3 distinct recommendations as a threaded reply/update
   **And** this can continue up to 12 distinct total for the same question context.

2.
   **Given** the system only has N distinct electricians worth recommending for the question (e.g., N=5)
   **When** the user clicks “More recommendations” enough times to exhaust the remaining distinct electricians
   **Then** the bot does not show (or removes) the “More recommendations” button on subsequent responses
   **And** it does not return duplicate electricians already shown in earlier pages.

3.
   **Given** a user clicks “More recommendations” multiple times for the same question context (including Telegram retry/double-delivery scenarios)
   **When** the callback handler is invoked with the same pagination cursor/context
   **Then** the pagination is idempotent: the user sees the same “next 3” set for that cursor
   **And** no duplicates are emitted across pages for that question context.

4.
   **Given** “More recommendations” results are returned
   **When** they are formatted
   **Then** they preserve citations + dates + cutoff timestamp formatting.

5.
   **Given** a user clicks “More recommendations”
   **When** results are returned
   **Then** this does not consume the per-channel daily question quota.

## Tasks / Subtasks

- [ ] Implement AC 1: the bot returns the next 3 distinct recommendations as a threaded reply/update (AC: 1)
  - [ ] Confirm UTC storage + IST presentation rules are followed
  - [ ] Add/adjust tests covering this AC
- [ ] Implement AC 2: the bot does not show (or removes) the “More recommendations” button on subsequent responses (AC: 2)
  - [ ] Confirm UTC storage + IST presentation rules are followed
  - [ ] Add/adjust tests covering this AC
- [ ] Implement AC 3: the pagination is idempotent: the user sees the same “next 3” set for that cursor (AC: 3)
  - [ ] Make operation idempotent and safe to retry
  - [ ] Add/adjust tests covering this AC
- [ ] Implement AC 4: they preserve citations + dates + cutoff timestamp formatting. (AC: 4)
  - [ ] Implement core behavior and error handling for this AC
  - [ ] Add/adjust tests covering this AC
- [ ] Implement AC 5: this does not consume the per-channel daily question quota. (AC: 5)
  - [ ] Implement core behavior and error handling for this AC
  - [ ] Add/adjust tests covering this AC
- [ ] Add regression/quality checks (lint/tests) and update docs if needed (AC: all)
  - [ ] Run the full test suite locally
  - [ ] Confirm no secrets leak into logs

## Dev Notes

- **Sources**:
  - Planning story: `/Users/Kuldeep_Desai/workspace/exp/tgbot/project_management/planning-artifacts/stories/epic-04/story-04-02-provide-more-recommendations-button-that-paginates-3-up-to-12-distinct.md`
  - Epics: `project_management/planning-artifacts/epics.md`
  - Architecture: `project_management/planning-artifacts/architecture.md`
- **Cross-cutting guardrails (from architecture/epics)**:
  - Use `uv` for dependency management; Python async-first; `aiogram==3.24.0`; `Telethon==1.42.0`.
  - Store timestamps in UTC; render IST only at presentation time.
  - Always escape dynamic text for Telegram MarkdownV2 using a single shared utility.
  - Maintain strict channel isolation (`channel_id` scoping) across retrieval/ranking/synthesis.
  - Emit structured logs and audit events with correlation/request IDs where applicable.

### References

- Story key: `4-2-provide-more-recommendations-button-that-paginates-3-up-to-12-distinct`
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
