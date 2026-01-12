---
epic: 1
epic_title: "Onboard a community channel and make the bot usable"
story: "1.3"
story_title: "`/help` returns usage instructions + channel disclaimer (threaded)"
source: "project_management/planning-artifacts/epics.md"
---

# Story 1.3: `/help` returns usage instructions + channel disclaimer (threaded)

### Story 1.3: `/help` returns usage instructions + channel disclaimer (threaded)
**FRs covered:** FR14

As a Busy Community Member,
I want to use `/help` to see how to ask questions and the channel’s disclaimer,
So that I know how to use the bot correctly and safely.

**Acceptance Criteria:**

**Given** the bot is running in a registered channel
**When** a user sends `/help`
**Then** the bot replies as a threaded reply (reply-to the `/help` message)
**And** includes usage instructions (how to ask questions)
**And** includes the per-channel disclaimer text stored for that channel.

**Given** the bot is running in a channel that is not registered
**When** a user sends `/help`
**Then** the bot replies as a threaded reply with a safe, minimal message indicating the channel is not configured
**And** it does not leak any other channel’s disclaimer.

**Given** `/help` output contains dynamic text (disclaimer or other values)
**When** the bot renders the reply
**Then** all dynamic text is correctly escaped for Telegram MarkdownV2 (no broken formatting).

