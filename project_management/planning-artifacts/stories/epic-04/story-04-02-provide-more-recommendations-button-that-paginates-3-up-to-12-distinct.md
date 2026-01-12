---
epic: 4
epic_title: "Explore more results and enforce per-channel daily quota"
story: "4.2"
story_title: "Provide “More recommendations” button that paginates +3 up to 12 distinct"
source: "project_management/planning-artifacts/epics.md"
---

# Story 4.2: Provide “More recommendations” button that paginates +3 up to 12 distinct

### Story 4.2: Provide “More recommendations” button that paginates +3 up to 12 distinct
**FRs covered:** FR24, FR25, FR26, FR27

As a Busy Community Member,
I want to request more recommendations beyond Top 3,
So that I can explore additional options without re-asking.

**Acceptance Criteria:**

**Given** an answer includes Top 3 recommendations
**When** the user clicks “More recommendations”
**Then** the bot returns the next 3 distinct recommendations as a threaded reply/update
**And** this can continue up to 12 distinct total for the same question context.

**Given** the system only has N distinct electricians worth recommending for the question (e.g., N=5)
**When** the user clicks “More recommendations” enough times to exhaust the remaining distinct electricians
**Then** the bot does not show (or removes) the “More recommendations” button on subsequent responses
**And** it does not return duplicate electricians already shown in earlier pages.

**Given** a user clicks “More recommendations” multiple times for the same question context (including Telegram retry/double-delivery scenarios)
**When** the callback handler is invoked with the same pagination cursor/context
**Then** the pagination is idempotent: the user sees the same “next 3” set for that cursor
**And** no duplicates are emitted across pages for that question context.

**Given** “More recommendations” results are returned
**When** they are formatted
**Then** they preserve citations + dates + cutoff timestamp formatting.

**Given** a user clicks “More recommendations”
**When** results are returned
**Then** this does not consume the per-channel daily question quota.

