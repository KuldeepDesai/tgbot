# Story 5.2: Quarantine unsafe ingested content and hard-filter it from answering

Status: done

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As a the system,
I want unsafe ingested content quarantined and excluded from normal retrieval and citations,
so that unsafe content is not amplified.

## Acceptance Criteria

1.
   **Given** ingested content is classified as quarantinable
   **When** it is processed into derived state
   **Then** it is marked quarantined with policy metadata.

2.
   **Given** a normal user query is processed
   **When** evidence is retrieved
   **Then** quarantined content is hard-filtered out and never cited.

## Tasks / Subtasks

- [ ] Implement AC 1: it is marked quarantined with policy metadata. (AC: 1)
  - [ ] Implement core behavior and error handling for this AC
  - [ ] Add/adjust tests covering this AC
- [ ] Implement AC 2: quarantined content is hard-filtered out and never cited. (AC: 2)
  - [ ] Implement core behavior and error handling for this AC
  - [ ] Add/adjust tests covering this AC
- [ ] Add regression/quality checks (lint/tests) and update docs if needed (AC: all)
  - [ ] Run the full test suite locally
  - [ ] Confirm no secrets leak into logs

## Dev Notes

- **Sources**:
  - Planning story: `/Users/Kuldeep_Desai/workspace/exp/tgbot/project_management/planning-artifacts/stories/epic-05/story-05-02-quarantine-unsafe-ingested-content-and-hard-filter-it-from-answering.md`
  - Epics: `project_management/planning-artifacts/epics.md`
  - Architecture: `project_management/planning-artifacts/architecture.md`
- **Cross-cutting guardrails (from architecture/epics)**:
  - Use `uv` for dependency management; Python async-first; `aiogram==3.24.0`; `Telethon==1.42.0`.
  - Store timestamps in UTC; render IST only at presentation time.
  - Always escape dynamic text for Telegram MarkdownV2 using a single shared utility.
  - Maintain strict channel isolation (`channel_id` scoping) across retrieval/ranking/synthesis.
  - Emit structured logs and audit events with correlation/request IDs where applicable.

### References

- Story key: `5-2-quarantine-unsafe-ingested-content-and-hard-filter-it-from-answering`
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
