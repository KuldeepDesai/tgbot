---
epic: 3
epic_title: "Ask questions in-channel and get evidence-backed answers (Top-3)"
story: "3.2"
story_title: "Send “typing…” immediately and reply in-thread with a safe fallback on failure"
source: "project_management/planning-artifacts/epics.md"
---

# Story 3.2: Send “typing…” immediately and reply in-thread with a safe fallback on failure

### Story 3.2: Send “typing…” immediately and reply in-thread with a safe fallback on failure
**FRs covered:** FR15, FR44

As a Busy Community Member,
I want immediate feedback that the bot is working and a clear reply even if something fails,
So that the experience feels responsive and reliable.

**Acceptance Criteria:**

**Given** a question is detected
**When** processing begins
**Then** the bot sends a Telegram “typing…” (chat action) promptly.

**Given** the answer flow succeeds
**When** the bot responds
**Then** it replies as a threaded reply to the user’s question message.

**Given** the answer flow fails at any point
**When** the bot responds
**Then** it replies as a threaded reply with: “Sorry, I couldn’t answer right now—please try again later.”

