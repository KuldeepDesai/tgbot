---
epic: 1
epic_title: "Onboard a community channel and make the bot usable"
story: "1.1"
story_title: "Set up initial project from the selected starter template"
source: "project_management/planning-artifacts/epics.md"
---

# Story 1.1: Set up initial project from the selected starter template

### Story 1.1: Set up initial project from the selected starter template
**FRs covered:** (Architecture prerequisite)

As a System Operator,
I want the project scaffolded using the approved architecture starter template,
So that the codebase is ready for implementing the bot and pipeline consistently.

**Acceptance Criteria:**

**Given** the architecture specifies Python + `uv` + `aiogram` + `Telethon` and a standard directory structure
**When** the project is initialized
**Then** the repo contains a Python project scaffold with dependency management in place (via `uv`)
**And** the bot and pipeline dependencies are added at the pinned versions specified in architecture (or documented equivalents if versions change).

**Given** the architecture defines standard module boundaries and entrypoints
**When** the scaffold is created
**Then** the project contains the expected source layout (e.g., `src/tgbot/...`), migrations skeleton, and runnable entrypoints for receiver/worker/ops.

