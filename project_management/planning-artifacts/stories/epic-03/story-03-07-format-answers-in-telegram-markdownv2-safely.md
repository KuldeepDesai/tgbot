---
epic: 3
epic_title: "Ask questions in-channel and get evidence-backed answers (Top-3)"
story: "3.7"
story_title: "Format answers in Telegram MarkdownV2 safely"
source: "project_management/planning-artifacts/epics.md"
---

# Story 3.7: Format answers in Telegram MarkdownV2 safely

### Story 3.7: Format answers in Telegram MarkdownV2 safely
**FRs covered:** FR16

As a Busy Community Member,
I want answers to render correctly in Telegram,
So that the content is readable and trustworthy.

**Acceptance Criteria:**

**Given** the bot formats any dynamic content (user query, message excerpts, entity names, disclaimers)
**When** the message is sent
**Then** all dynamic text is escaped using a single shared Telegram MarkdownV2 escape utility.

**Given** formatting errors would break rendering
**When** invalid markdown would otherwise be produced
**Then** the system avoids sending broken markup (escape-first, fail-safe behavior).

