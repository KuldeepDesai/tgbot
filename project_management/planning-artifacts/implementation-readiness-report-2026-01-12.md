---
stepsCompleted: [1, 2, 3, 4, 5, 6]
inputDocuments:
  - project_management/planning-artifacts/prd.md
  - project_management/planning-artifacts/architecture.md
  - project_management/planning-artifacts/epics.md
date: 2026-01-12
author: Kuldeep
---

# Implementation Readiness Assessment Report

**Date:** 2026-01-12  
**Project:** tgbot

## Document Discovery

## PRD Files Found

**Whole Documents:**
- `prd.md` (size: 20650 bytes, modified: Jan 12 18:45:37 2026)

**Sharded Documents:**
- None found

## Architecture Files Found

**Whole Documents:**
- `architecture.md` (size: 35384 bytes, modified: Jan 12 18:45:36 2026)

**Sharded Documents:**
- None found

## Epics & Stories Files Found

**Whole Documents:**
- `epics.md` (size: 36710 bytes, modified: Jan 12 19:30:34 2026)

**Sharded Documents:**
- None found

## UX Design Files Found

**Whole Documents:**
- None found

**Sharded Documents:**
- None found

## Issues Found

- ⚠️ **WARNING: UX design document not found** (no `{planning_artifacts}/*ux*.md` or `{planning_artifacts}/*ux*/index.md` matches)

## Required Actions

- Confirm the documents above are the intended sources for the readiness assessment.
- If you *do* have UX artifacts elsewhere (or you want them considered), point me to the path(s) and I’ll include them in the inventory.

**Document Discovery Complete**

**Ready to proceed?** [C] Continue to PRD Analysis

**Select an Option:** [C] Continue to File Validation / PRD Analysis

## PRD Analysis

### Functional Requirements

## Functional Requirements Extracted

FR1: System Operator can register a Telegram channel for use by the bot.  
FR2: System Operator can set a per-channel disclaimer text during onboarding.  
FR3: System Operator can update a channel’s disclaimer text via configuration (effective after app restart).  
FR4: System can associate incoming Telegram updates to a known channel record (for multi-channel operation).  
FR5: System can ingest new messages from each onboarded channel.  
FR6: System can backfill historical messages for an onboarded channel.  
FR7: System can persist ingested messages with message metadata (chat/channel id, message id, user id, timestamp).  
FR8: System can record message edits as updates to prior messages.  
FR9: System can record message deletions (when detectable) and prevent deleted messages from being used as evidence in answers.  
FR10: System can retain stored channel data indefinitely unless manually deleted outside the system.  
FR11: Busy Community Member can ask a question by mentioning the bot in a channel message.  
FR12: Busy Community Member can ask a question by replying to the bot in a channel thread.  
FR13: System can ignore messages that are neither a bot mention nor a reply-to-bot (not treated as a question).  
FR14: Busy Community Member can request usage instructions via `/help`.  
FR15: System can respond to a question with a threaded reply in the same channel.  
FR16: System can format answers using Telegram MarkdownV2.  
FR17: System can include Top 3 recommendations in an answer when applicable.  
FR18: System can include citations for answer content (Telegram message link when possible; fallback citation otherwise).  
FR19: System can include message dates alongside citations.  
FR20: System can include an “as-of cutoff” timestamp (IST) in every answer (e.g., “Based on messages up to … (IST)”).  
FR21: System can extract and display contact details when they are present in source messages.  
FR22: System can avoid fabricating contact details when none exist in sources.  
FR23: System can handle “conflicting recommendations” by presenting Top 3 while explicitly reflecting disagreement and supporting evidence.  
FR24: Busy Community Member can request more recommendations via an inline “More recommendations” button.  
FR25: System can return the next 3 distinct recommendations per click, up to 12 distinct total for the same question context.  
FR26: System can ensure “More recommendations” results preserve citations + dates + cutoff timestamp formatting.  
FR27: System can ensure “More recommendations” does not consume daily quota.  
FR28: System can enforce a per-channel daily question quota (default 50/day/channel).  
FR29: System can reset a channel’s quota at midnight India time.  
FR30: System can inform users when a channel’s daily quota is exhausted and refuse additional questions until reset.  
FR31: Busy Community Member can provide feedback on answers via 👍/👎 reactions on the bot’s answer message.  
FR32: System can record feedback events for later analysis.  
FR33: System can evaluate user queries against safety policies and refuse to answer when required.  
FR34: System can quarantine safety-flagged ingested content so it is excluded from normal answering.  
FR35: System can detect bot removal from a channel when Telegram provides such signals.  
FR36: System can detect bot permission changes when Telegram provides such signals.  
FR37: System can create an audit event when the bot is removed from a channel.  
FR38: System can create an audit event when the bot’s permissions change in a channel.  
FR39: System can stop ingesting from a channel after bot removal (or adjust behavior appropriately after permission loss).  
FR40: System Operator can send a message to a specific onboarded channel outside the normal Q&A flow.  
FR41: System Operator can broadcast a message to all onboarded channels outside the normal Q&A flow.  
FR42: System Operator can trigger out-of-band messaging via an ops CLI.  
FR43: System Operator can trigger out-of-band messaging via an internal-only HTTP endpoint.  
FR44: System can notify the user when it cannot produce an answer and ask them to try again later.

Total FRs: 44

### Non-Functional Requirements

## Non-Functional Requirements Extracted

NFR1 (Performance - Latency MVP): Average end-to-end answer latency is < 5 seconds.  
NFR2 (Performance - Tail latency MVP): P95 end-to-end answer latency is ≤ 15 seconds.  
NFR3 (Performance - User feedback during processing): The bot must provide immediate feedback via Telegram “typing…” while processing.  
NFR4 (Reliability - Degrade gracefully): If an answer cannot be produced, respond with a clear fallback (“try again later”) rather than failing silently.  
NFR5 (Security - Channel isolation): The system must prevent cross-channel leakage (answers must only use evidence from the channel where the question was asked).  
NFR6 (Security - Secrets handling): Provider API keys/secrets must not be exposed in logs or bot responses.  
NFR7 (Security - Internal operator endpoint): Network-restricted access is sufficient for MVP (no additional auth required).  
NFR8 (Scalability - Channel scale MVP): Support up to 5 onboarded channels per system instance with acceptable performance (per the latency targets).  
NFR9 (Integration - Robustness): Telegram integration must be robust under normal API/network variability (retries/backoff as appropriate), without compromising channel isolation.  
NFR10 (Observability): The system must emit structured logs and include correlation IDs to support troubleshooting and auditing (especially for “bot not responding”, quota enforcement, and channel membership/permission changes).

Total NFRs: 10

### Additional Requirements (non FR/NFR-labeled constraints & scope)

- Hard requirement: citations + dates on every answer.
- Hard requirement: channel-scoped answers only (no cross-channel leakage) for MVP.
- Hard requirement: safety gate with quarantine/refusal behavior.
- Retention: keep data forever for MVP; deletion requests handled manually outside the system.
- Interaction constraints: in-channel Q&A only (no DMs); replies should be threaded; output format is Telegram MarkdownV2.
- `/help` behavior: show a per-channel disclaimer loaded from DB.
- Answer format must include: “Based on messages up to <cutoff> (IST)” line; post‑MVP timezone becomes per-channel setting.
- Quota policy: 50 questions/day/channel, reset at midnight India time; quota exceeded message; “More recommendations” does not consume quota.
- Ops: operator-grade CLI/logs for onboarding/troubleshooting; ops-only broadcast/per-channel messaging via CLI + internal-only endpoint.
- Post-MVP features explicitly out of scope: WhatsApp ingestion, admin tooling/config UI, language improvements (e.g., Hinglish), latency optimization target <3s avg.

### PRD Completeness Assessment

- PRD is unusually implementation-friendly: explicit FR list (44) and NFR list (10), plus clear MVP scope and success criteria.
- Key dependency wording to resolve during implementation: multiple requirements are conditional on “when Telegram provides such signals” (bot removal/permission changes, deletions). Define detectable vs non-detectable behavior explicitly in epics/stories and architecture.

## Epic Coverage Validation

### Epic FR Coverage Extracted (from `epics.md`)

FR1: Epic 1 — Register channel  
FR2: Epic 1 — Set disclaimer  
FR3: Epic 1 — Update disclaimer  
FR4: Epic 1 — Associate updates to channel record  
FR5: Epic 2 — Ingest new messages  
FR6: Epic 2 — Backfill history  
FR7: Epic 2 — Persist messages + metadata  
FR8: Epic 2 — Record edits  
FR9: Epic 2 — Record deletions (when detectable) + exclude from evidence  
FR10: Epic 2 — Retain data indefinitely  
FR11: Epic 3 — Ask via bot mention  
FR12: Epic 3 — Ask via reply-to-bot  
FR13: Epic 3 — Ignore non-question messages  
FR14: Epic 1 — `/help` usage instructions  
FR15: Epic 3 — Threaded replies  
FR16: Epic 3 — MarkdownV2 formatting  
FR17: Epic 3 — Top 3 recommendations  
FR18: Epic 3 — Citations (link or fallback)  
FR19: Epic 3 — Dates alongside citations  
FR20: Epic 3 — Cutoff timestamp line (IST)  
FR21: Epic 3 — Extract/display contacts when present  
FR22: Epic 3 — No fabricated contacts  
FR23: Epic 3 — Handle conflicting recommendations  
FR24: Epic 4 — “More recommendations” button  
FR25: Epic 4 — Next 3 per click up to 12 distinct  
FR26: Epic 4 — Preserve citations/dates/cutoff in pagination  
FR27: Epic 4 — Pagination does not consume quota  
FR28: Epic 4 — Per-channel daily quota enforcement  
FR29: Epic 4 — Reset quota midnight IST  
FR30: Epic 4 — Quota exhausted messaging + refusal  
FR31: Epic 5 — 👍/👎 feedback via reactions  
FR32: Epic 5 — Record feedback events  
FR33: Epic 5 — Query safety evaluation + refusal  
FR34: Epic 5 — Quarantine flagged ingested content from answering  
FR35: Epic 6 — Detect bot removal (when available)  
FR36: Epic 6 — Detect permission changes (when available)  
FR37: Epic 6 — Audit event on removal  
FR38: Epic 6 — Audit event on permission change  
FR39: Epic 6 — Stop/degrade ingestion after removal/permission loss  
FR40: Epic 6 — Ops message to a specific channel  
FR41: Epic 6 — Ops broadcast message  
FR42: Epic 6 — Trigger ops messaging via CLI  
FR43: Epic 6 — Trigger ops messaging via internal-only HTTP endpoint  
FR44: Epic 3 — “Try again later” failure handling

Total FRs in epics: 44

### Coverage Matrix

| FR Number | PRD Requirement (summary) | Epic Coverage | Status |
| --------- | -------------------------- | ------------ | ------ |
| FR1 | System Operator can register a Telegram channel for use by the bot. | Epic 1 | ✓ Covered |
| FR2 | System Operator can set a per-channel disclaimer text during onboarding. | Epic 1 | ✓ Covered |
| FR3 | System Operator can update a channel’s disclaimer text via configuration (effective after app restart). | Epic 1 | ✓ Covered |
| FR4 | System can associate incoming Telegram updates to a known channel record (for multi-channel operation). | Epic 1 | ✓ Covered |
| FR5 | System can ingest new messages from each onboarded channel. | Epic 2 | ✓ Covered |
| FR6 | System can backfill historical messages for an onboarded channel. | Epic 2 | ✓ Covered |
| FR7 | System can persist ingested messages with message metadata (chat/channel id, message id, user id, timestamp). | Epic 2 | ✓ Covered |
| FR8 | System can record message edits as updates to prior messages. | Epic 2 | ✓ Covered |
| FR9 | System can record message deletions (when detectable) and prevent deleted messages from being used as evidence in answers. | Epic 2 | ✓ Covered |
| FR10 | System can retain stored channel data indefinitely unless manually deleted outside the system. | Epic 2 | ✓ Covered |
| FR11 | Busy Community Member can ask a question by mentioning the bot in a channel message. | Epic 3 | ✓ Covered |
| FR12 | Busy Community Member can ask a question by replying to the bot in a channel thread. | Epic 3 | ✓ Covered |
| FR13 | System can ignore messages that are neither a bot mention nor a reply-to-bot (not treated as a question). | Epic 3 | ✓ Covered |
| FR14 | Busy Community Member can request usage instructions via `/help`. | Epic 1 | ✓ Covered |
| FR15 | System can respond to a question with a threaded reply in the same channel. | Epic 3 | ✓ Covered |
| FR16 | System can format answers using Telegram MarkdownV2. | Epic 3 | ✓ Covered |
| FR17 | System can include Top 3 recommendations in an answer when applicable. | Epic 3 | ✓ Covered |
| FR18 | System can include citations for answer content (Telegram message link when possible; fallback citation otherwise). | Epic 3 | ✓ Covered |
| FR19 | System can include message dates alongside citations. | Epic 3 | ✓ Covered |
| FR20 | System can include an “as-of cutoff” timestamp (IST) in every answer (e.g., “Based on messages up to … (IST)”). | Epic 3 | ✓ Covered |
| FR21 | System can extract and display contact details when they are present in source messages. | Epic 3 | ✓ Covered |
| FR22 | System can avoid fabricating contact details when none exist in sources. | Epic 3 | ✓ Covered |
| FR23 | System can handle “conflicting recommendations” by presenting Top 3 while explicitly reflecting disagreement and supporting evidence. | Epic 3 | ✓ Covered |
| FR24 | Busy Community Member can request more recommendations via an inline “More recommendations” button. | Epic 4 | ✓ Covered |
| FR25 | System can return the next 3 distinct recommendations per click, up to 12 distinct total for the same question context. | Epic 4 | ✓ Covered |
| FR26 | System can ensure “More recommendations” results preserve citations + dates + cutoff timestamp formatting. | Epic 4 | ✓ Covered |
| FR27 | System can ensure “More recommendations” does not consume daily quota. | Epic 4 | ✓ Covered |
| FR28 | System can enforce a per-channel daily question quota (default 50/day/channel). | Epic 4 | ✓ Covered |
| FR29 | System can reset a channel’s quota at midnight India time. | Epic 4 | ✓ Covered |
| FR30 | System can inform users when a channel’s daily quota is exhausted and refuse additional questions until reset. | Epic 4 | ✓ Covered |
| FR31 | Busy Community Member can provide feedback on answers via 👍/👎 reactions on the bot’s answer message. | Epic 5 | ✓ Covered |
| FR32 | System can record feedback events for later analysis. | Epic 5 | ✓ Covered |
| FR33 | System can evaluate user queries against safety policies and refuse to answer when required. | Epic 5 | ✓ Covered |
| FR34 | System can quarantine safety-flagged ingested content so it is excluded from normal answering. | Epic 5 | ✓ Covered |
| FR35 | System can detect bot removal from a channel when Telegram provides such signals. | Epic 6 | ✓ Covered |
| FR36 | System can detect bot permission changes when Telegram provides such signals. | Epic 6 | ✓ Covered |
| FR37 | System can create an audit event when the bot is removed from a channel. | Epic 6 | ✓ Covered |
| FR38 | System can create an audit event when the bot’s permissions change in a channel. | Epic 6 | ✓ Covered |
| FR39 | System can stop ingesting from a channel after bot removal (or adjust behavior appropriately after permission loss). | Epic 6 | ✓ Covered |
| FR40 | System Operator can send a message to a specific onboarded channel outside the normal Q&A flow. | Epic 6 | ✓ Covered |
| FR41 | System Operator can broadcast a message to all onboarded channels outside the normal Q&A flow. | Epic 6 | ✓ Covered |
| FR42 | System Operator can trigger out-of-band messaging via an ops CLI. | Epic 6 | ✓ Covered |
| FR43 | System Operator can trigger out-of-band messaging via an internal-only HTTP endpoint. | Epic 6 | ✓ Covered |
| FR44 | System can notify the user when it cannot produce an answer and ask them to try again later. | Epic 3 | ✓ Covered |

### Missing Requirements

- None. All PRD FRs (FR1–FR44) have an explicit epic mapping in `epics.md`.

### Coverage Statistics

- Total PRD FRs: 44
- FRs covered in epics: 44
- Coverage percentage: 100%

## UX Alignment Assessment

### UX Document Status

- Not Found (no dedicated UX document in `project_management/planning-artifacts/`).

### Alignment Issues

- No major misalignment detected for MVP: PRD defines a **Telegram text-only interface** and includes core interaction UX directly (pinned bot, threaded replies, MarkdownV2, inline “More recommendations” button, “typing…” while processing).
- Architecture explicitly supports these Telegram UX behaviors (threaded replies, inline callbacks, MarkdownV2 escaping, typing indicator, quota messaging, cutoff timestamp line).

### Warnings

- While a separate UX doc is not strictly required for a Telegram text-only MVP, you may still want a lightweight “Bot UX Spec” appendix to lock down:
  - message templates (happy path + errors),
  - MarkdownV2 escaping rules,
  - button labels/callback behavior,
  - citation/date formatting and cutoff timestamp line formatting.

## Epic Quality Review (create-epics-and-stories standards)

### Best-Practices Assessment (high-level)

- Epics are **user/outcome oriented** (no “setup DB” / “infra only” epics). Even the “pipeline” work is framed as enabling replayable, trustworthy answers and operator workflows.
- No “Epic N depends on Epic N+1” style forward dependency issues found; later epics build on earlier ones as expected.
- Stories consistently include:
  - a clear role/value statement (“As a … I want … so that …”)
  - explicit **FR coverage** mapping
  - **testable** BDD-style acceptance criteria (Given/When/Then)

### 🔴 Critical Violations

- None found.

### 🟠 Major Issues (should be clarified before implementation to avoid rework)

1. **“When detectable” requirements need an implementation policy**
   - Deletions, bot removal, and permission-change signals are conditional on what Telegram surfaces.
   - Recommendation: document a clear policy in stories/architecture for:
     - best-effort detection via Bot API,
     - reconciliation via userbot where feasible,
     - fallback behavior when signals are not available.

### Clarifications Captured (from implementation readiness review)

- **“Distinct recommendation” semantics (dedup)**: If multiple messages refer to the same electrician/provider, they should appear **only once** in results; other results should be **different electricians**.
- **“More recommendations” exhaustion behavior**: If fewer than the maximum distinct recommendations exist (e.g., only 5 total), the bot should **stop offering** the “More recommendations” button once exhausted (no empty/no-op pagination).
- **Pagination idempotency**: Repeated clicks / Telegram retry/double-delivery for the same question context must be **idempotent** (same cursor → same next set; no duplicates across pages).
- **Audit events on detectable lifecycle changes**: Any detectable channel lifecycle changes (e.g., bot removal, permission changes; and message lifecycle signals where available) should be **documented and recorded as audit events**.

### 🟡 Minor Concerns (nice-to-fix; not blockers)

- Some stories cover NFRs/constraints without explicitly tagging them (e.g., isolation, idempotency, observability). Consider adding a small “NFRs covered” line where relevant for traceability completeness.
- A few system-heavy stories (e.g., envelope normalization + lake + latest-state) are substantial; if you want smoother execution tracking, consider splitting into smaller stories per deliverable while preserving independence.

## Summary and Recommendations

### Overall Readiness Status

READY (with a few clarifications recommended before you start coding)

### Critical Issues Requiring Immediate Action

- None identified.

### Recommended Next Steps

1. Decide and document **“distinct recommendation”** semantics + dedup logic (impacts Epic 3 + Epic 4 correctness).
2. Specify **pagination cursor/query context** behavior for “More recommendations” (idempotent, retry-safe, no duplicates).
3. Lock down “**when detectable**” policies for deletions + membership/permission changes (Bot API vs userbot vs no-signal fallback).
4. Optional: add a 1–2 page **Bot UX Spec** appendix (message templates, formatting rules, button labels/callback UX).

### Final Note

This assessment identified 0 critical violations, 3 major clarifications, and 2 minor improvements. You can proceed to implementation now, but addressing the major clarifications early will prevent churn in retrieval/pagination, and in “best-effort” Telegram lifecycle handling.

