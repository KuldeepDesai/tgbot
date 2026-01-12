---
epic: 3
epic_title: "Ask questions in-channel and get evidence-backed answers (Top-3)"
story: "3.4"
story_title: "Retrieve, rank, and return Top 3 distinct recommendations with citations and dates"
source: "project_management/planning-artifacts/epics.md"
---

# Story 3.4: Retrieve, rank, and return Top 3 distinct recommendations with citations and dates

### Story 3.4: Retrieve, rank, and return Top 3 distinct recommendations with citations and dates
**FRs covered:** FR17, FR18, FR19

As a Busy Community Member,
I want the bot to return the Top 3 most relevant recommendations backed by evidence,
So that I can act quickly with confidence.

**Acceptance Criteria:**

**Given** a question is detected in a registered channel
**When** the system processes it
**Then** it retrieves relevant content for that channel and returns 3 distinct recommendations when applicable.

**Given** multiple evidence messages refer to the same underlying electrician (same provider)
**When** the system forms the Top 3 list
**Then** that electrician appears at most once in the results (deduplicated)
**And** the remaining items (if available) are different electricians.

**Given** a recommendation is presented
**When** the bot formats the answer
**Then** each item includes citations (Telegram message link when possible; fallback citation otherwise) and message dates.

**Given** there are fewer than 3 strong results
**When** the bot responds
**Then** it returns the best available results without fabricating missing recommendations.

