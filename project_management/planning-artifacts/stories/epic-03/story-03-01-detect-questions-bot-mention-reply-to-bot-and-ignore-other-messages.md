---
epic: 3
epic_title: "Ask questions in-channel and get evidence-backed answers (Top-3)"
story: "3.1"
story_title: "Detect questions (bot mention / reply-to-bot) and ignore other messages"
source: "project_management/planning-artifacts/epics.md"
---

# Story 3.1: Detect questions (bot mention / reply-to-bot) and ignore other messages

### Story 3.1: Detect questions (bot mention / reply-to-bot) and ignore other messages
**FRs covered:** FR11, FR12, FR13

As a Busy Community Member,
I want my question to be recognized when I mention the bot or reply-to-bot,
So that the bot responds only when I’m actually asking it a question.

**Acceptance Criteria:**

**Given** the bot receives a message update in a registered channel
**When** the message is a bot mention
**Then** the system treats it as a question and starts the answer flow.

**Given** the bot receives a message update in a registered channel
**When** the message is a reply to a prior bot message
**Then** the system treats it as a question and starts the answer flow.

**Given** the bot receives a message update in a registered channel
**When** the message is neither a bot mention nor a reply-to-bot
**Then** the system does not treat it as a question and does not respond.

