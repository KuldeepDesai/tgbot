---
stepsCompleted:
  - step-01-init
  - step-02-discovery
  - step-03-success
  - step-04-journeys
  - step-05-domain
  - step-06-innovation
  - step-07-project-type
  - step-08-scoping
  - step-09-functional
  - step-10-nonfunctional
  - step-11-polish
inputDocuments:
  - project_management/planning-artifacts/product-brief-tgbot-2026-01-12.md
  - project_management/planning-artifacts/research/technical-telegram-ingestion-pipeline-research-2026-01-12.md
  - project_management/analysis/brainstorming-session-2026-01-12.md
workflowType: 'prd'
classification:
  projectType: api_backend
  domain: community/property (gated community) knowledge & Q&A
  complexity: medium
  projectContext: greenfield
documentCounts:
  briefCount: 1
  researchCount: 1
  brainstormingCount: 1
  projectDocsCount: 0
---

# Product Requirements Document - tgbot

**Author:** Kuldeep
**Date:** 2026-01-12

## Success Criteria

### User Success

- **Speed (MVP):** Users receive **Top 3** relevant answers in **under 5 seconds on average**.
- **Speed (post-MVP optimization):** Improve average latency to **under 3 seconds** once usefulness is validated.
- **Trust/traceability:** Every answer includes **citations** (Telegram message link when possible; otherwise a fallback citation) and includes **message dates**.

### Business Success

- **Adoption:** Reach **10–15 queries/day per channel** by **month 3**.
- **Engagement (WAU):** Reach **20 WAU per channel** by **month 3**, where **WAU = unique users who either ask a question OR react 👍/👎 on bot answers**.

### Technical Success

- **Citations + dates on every answer** (hard requirement).
- **Channel-scoped answers only**: no cross-channel leakage for MVP (hard requirement).
- **Safety gate**: message + query safety with **quarantine/refusal behavior** (hard requirement).

### Measurable Outcomes

- Avg answer latency < 5 seconds (Top-3 response) for MVP; < 3 seconds is a post-MVP optimization target.
- ≥ 40% 👍 among rated responses (first 3 months; among rated).
- 10–15 queries/day/channel by month 3.
- 20 WAU/channel by month 3 (as defined above).

## Product Scope

### MVP - Minimum Viable Product

- Telegram ingestion (multi-channel, channels-only model)
- In-channel Q&A (no DMs)
- Top-3 ranked results
- Evidence/citations + dates
- Contact extraction when present
- Feedback capture via 👍/👎 reactions on bot answers
- Channel-scoped retrieval only (no cross-channel leakage)
- Safety gate with quarantine/refusal behavior

### Growth Features (Post-MVP)

- WhatsApp ingestion

### Vision (Future)

- Multi-channel expansion beyond Telegram/WhatsApp (e.g., email)
- Richer admin tooling / configuration
- Improved language support (e.g., Hinglish) if/when it’s worth the complexity

## User Journeys

### Journey 1 — Busy Community Member (Primary Success Path): “Recommended electrician”

**Opening scene:** A busy resident is in a high-volume gated community Telegram channel. The bot is **pinned**, so it’s the obvious “ask here” entry point. A minor electrical issue becomes urgent, and scrolling/search feels hopeless.  
**Rising action:** They ask in-channel: “recommended electrician” and expect an answer that’s fast and trustworthy.  
**Climax:** The bot replies **in a thread** with:
- **Top 3** recommendations, each including a short “why”, **citations + dates** (link when possible; otherwise fallback), and **contact details when present**
- an inline **“More recommendations”** button that loads the **next 3** recommendations per click, up to **12 distinct recommendations** total  
**Resolution:** The user quickly decides who to call and feels confident because they can verify source messages.

### Journey 2 — Busy Community Member (Primary Edge Case): Conflicting recommendations

**Opening scene:** Same user, but the community’s history shows disagreement.  
**Rising action:** They need help navigating trade-offs, not a wall of chat snippets.  
**Climax:** The bot still returns **Top 3**, explicitly calls out disagreement neutrally, shows **citations + dates** supporting each side, and offers **“More recommendations”** (+3 at a time) up to **12 distinct**.  
**Resolution:** The user makes a decision faster because the conflict is structured and evidence-backed.

### Journey 3 — System Operator (Onboarding / Setup): “Bot starts ingesting new messages”

**Opening scene:** A system operator manually onboards a community (manual is fine for MVP; scripts may exist outside the repo).  
**Rising action:** They connect the bot to the community channel(s).  
**Climax (success moment):** They see **CLI/log output** indicating ingestion is active.  
**Resolution:** They have enough confidence without dashboards/admin UI.

### Journey 4 — System Operator (Support/Troubleshooting): “Bot not responding”

**Opening scene:** Members say the bot stopped replying in-channel.  
**Rising action:** Operator checks **CLI/logs** to distinguish process down vs delivery issues vs handler errors vs rate limits.  
**Climax:** Operator restores responsiveness and verifies with a simple known query and a successful threaded reply.  
**Resolution:** Repeatable troubleshooting loop with minimal operator burden.

### Journey Requirements Summary

- Pinned bot discoverability
- Threaded replies
- Top-3 recommendation format + **“More recommendations”** button (**+3** up to **12 distinct**)
- Evidence-first answers: citations + dates on every answer (link or fallback)
- Contact extraction when present; no fabrication when missing
- Conflict-aware formatting (explicit disagreement + evidence)
- Channel-scoped retrieval (no cross-channel leakage)
- Operator-grade logs for onboarding + troubleshooting

## Domain-Specific Requirements

### Compliance & Regulatory

- None (MVP). For our gated community knowledge & Q&A domain, there are no special compliance requirements beyond standard platform usage and the product’s channel isolation rule.

### Technical Constraints

- **No cross-channel leakage (hard requirement):** Answers must only use evidence from the channel where the question was asked.
- **Channel membership boundary (“standard” consent):** The bot only ingests/answers in channels where it is explicitly added.
- **Retention:** Keep data **forever** for MVP; deletion requests are handled **manually outside the system**.

### Integration Requirements

- Telegram-only for MVP (WhatsApp ingestion is post-MVP).

### Risk Mitigations

- **Cross-channel leakage risk:** Treat channel scope as a first-class filter in retrieval/ranking/synthesis; add guardrails/tests to prevent accidental mixing.
- **Deletion requests:** Document a simple system-operator runbook/process for handling deletion outside the system.

## Innovation & Novel Patterns

### Detected Innovation Areas

- **Meaningful, decision-ready answers from noisy chat history**: users get consolidated recommendations instead of searching and reading dozens of messages.
- **Evidence-backed trust pattern**: every answer carries citations + dates, keeping the synthesis verifiable.
- **Telegram-native consumption UX**: **Top 3** by default, with a **“More recommendations”** button to fetch the next **3** at a time, up to **12 distinct** results.

### Market Context & Competitive Landscape

- Existing behavior is “search + scroll” (fragmented retrieval). Our differentiation is **consolidation into an answer** that’s usable immediately, while staying evidence-backed.

### Validation Approach

- **Pilot in 1 channel** and validate the core assumption (“community knowledge can be consolidated reliably”) via:
  - **WAU ≥ 20 per channel by month 3** (WAU = unique users who ask OR react 👍/👎 on bot answers)

### Risk Mitigation

- **If consolidation isn’t reliable enough:** fall back to **best-matching messages/snippets with citations** (still evidence-first, but reduced synthesis).

## API Backend Specific Requirements

### Project-Type Overview

- **Interface:** Telegram bot only (text-only).
- **Primary interaction:** Users ask questions in natural language in-channel; bot replies in a **thread**.
- **Commands:** Only **`/help`** (instructs users to ask in natural language + shows a **per-channel disclaimer** loaded from DB).
- **Auth model:** **Membership-only** (Telegram channel membership boundary; no extra gating).
- **Output format:** Telegram **MarkdownV2**.
- **Cutoff timestamp (must show on answers):** Every answer must show: **“Based on messages up to \<cutoff\> (IST)”**. Post‑MVP, cutoff timezone becomes a **per-channel setting**.

### Technical Architecture Considerations

- **Update delivery:** **Long polling** (no inbound public webhook endpoint for MVP).
- **Channel isolation:** Hard requirement — answers must only use evidence from the **current channel** (no cross-channel leakage).
- **Async response UX:**
  - Immediately send **Telegram “typing…” chat action**.
  - Then send the final answer as a **threaded reply**.
  - If processing fails: reply with **“Sorry, I couldn’t answer right now—please try again later.”**
- **Quota / rate limiting (MVP):**
  - No per-user rate limits.
  - Enforce **per-channel quota: 50 questions/day**, reset automatically at **midnight India time**.
  - When quota is exhausted, reply that the **daily quota is over**.
- **Bot membership + permissions audit & behavior:**
  - If bot is **removed** (left/kicked) from a channel **and Telegram exposes this**, create an **audit event** and **stop trying to ingest** from that channel.
  - If bot’s **permissions change** (e.g., loses read access), create an **audit event** and adjust ingestion/processing so we don’t keep failing noisily.

### Endpoint / Interaction Specs (`endpoint_specs`)

- **Natural-language question handler:** Any text message treated as a query.
- **`/help` handler:** Returns usage instructions + per-channel disclaimer (from DB).
- **Inline callbacks:**
  - **“More recommendations”** button returns the next **3** recommendations per click, up to **12 distinct** total, maintaining citations + dates + cutoff timestamp.
- **Operator message send (out-of-band / ops-only):**
  - **CLI command** to send:
    - broadcast message to *all* channels where bot is present, or
    - message to a *specific* channel.
  - **Internal-only HTTP endpoint** (curl/Postman) providing the same ability (not a public product API).

### Authentication Model (`auth_model`)

- Rely on Telegram’s channel membership boundary (**membership-only**).
- No user accounts, roles, or admin-only query gating in MVP.

### Data Schemas (`data_schemas`)

- **Input:** Telegram message text + metadata (chat/channel id, user id, message id, timestamp).
- **Output:** MarkdownV2 message containing:
  - cutoff timestamp line: **“Based on messages up to … (IST)”**
  - Top 3 recommendations (+ optional “More recommendations” pagination up to 12)
  - citations (link when possible; fallback citation otherwise) + dates
  - contact details when present

### Error Codes / Failure Handling (`error_codes`)

- **Quota exceeded:** “Daily quota is over; try again after midnight IST.”
- **Processing failure:** “Sorry, I couldn’t answer right now—please try again later.”
- **Formatting safety:** ensure MarkdownV2 escaping to avoid broken rendering.
- **Bot removed/permission reduced:** audit event recorded; ingestion disabled or degraded appropriately.

### Rate Limits (`rate_limits`)

- **Per-channel daily quota** (50/day), reset at midnight IST.
- No per-user throttling for MVP.

### API Docs (`api_docs`)

- No external/public API or SDK in MVP.
- Document bot behaviors, message formats (incl cutoff timestamp), quota policy, and ops-only broadcast mechanisms.

## Project Scoping & Phased Development

### MVP Strategy & Philosophy

- **MVP Approach:** **Problem-solving MVP** (prove usefulness fast in a real channel)
- **Resource Requirements:** **Solo dev**
  - Telegram bot integration (long polling)
  - Backfill + ingestion pipeline basics
  - Retrieval/ranking + answer formatting (MarkdownV2)
  - Quota + basic audit events
  - Minimal ops tooling (CLI + internal endpoint for broadcasts)

### MVP Feature Set (Phase 1)

**Core User Journeys Supported:**

- **Busy Community Member**
  - Ask natural language question in-channel → bot replies in thread with **Top 3**
  - **More recommendations** button loads +3 up to **12 distinct**
  - Every answer includes **citations + dates** and an **“as-of cutoff” timestamp (IST)**

**Must-Have Capabilities:**

- Telegram **text-only** Q&A, **threaded replies**
- **`/help`** command only (disclaimer from DB; load at startup is OK)
- **Long polling** (no inbound public webhook endpoint for MVP)
- **Historical backfill included**
- **Channel-scoped retrieval only** (no cross-channel leakage)
- **Answer format**: **MarkdownV2**, citations + dates, cutoff timestamp
- **Async UX**: show **typing action**, then post final answer; failures return “try again later”
- **Per-channel daily quota**: **50 questions/day**, reset **midnight IST**; quota exhaustion message
- **Bot removed / permission change detection** (if Telegram exposes it): create **audit events** and **stop ingestion / adjust behavior**
- **Ops messaging** (outside normal flow): **CLI + internal-only endpoint** to send broadcast or per-channel messages

### Post-MVP Features

**Phase 2 (Post-MVP):**

- **WhatsApp ingestion** (priority)
- Latency optimization from **<5s avg (MVP)** toward **<3s avg**
- Channel-configurable timezone for cutoff timestamps / quota reset time

**Phase 3 (Expansion):**

- Multi-channel expansion beyond Telegram/WhatsApp (e.g., email)
- Richer admin tooling / configuration UI
- Language improvements (e.g., Hinglish)

### Risk Mitigation Strategy

- **Technical Risks:** backfill complexity; maintaining channel isolation; quota reset correctness (midnight IST); keeping answers responsive (MVP target **<5s avg**).
- **Market Risks:** WAU might not reach **≥ 20** in 1-channel pilot by month 3 → adjust UX/content strategy; use fallback “best matching messages” if consolidation isn’t reliable.
- **Resource Risks:** solo dev capacity → keep features minimal, avoid dashboards/admin UI, defer optimizations (<3s) and expansions (WhatsApp) to Phase 2.

## Functional Requirements

### Channel Onboarding & Configuration

- FR1: System Operator can register a Telegram channel for use by the bot.
- FR2: System Operator can set a **per-channel disclaimer text** during onboarding.
- FR3: System Operator can update a channel’s disclaimer text via configuration (effective after app restart).
- FR4: System can associate incoming Telegram updates to a known channel record (for multi-channel operation).

### Ingestion, Backfill, and Message Lifecycle

- FR5: System can ingest new messages from each onboarded channel.
- FR6: System can backfill historical messages for an onboarded channel.
- FR7: System can persist ingested messages with message metadata (chat/channel id, message id, user id, timestamp).
- FR8: System can record message edits as updates to prior messages.
- FR9: System can record message deletions (when detectable) and prevent deleted messages from being used as evidence in answers.
- FR10: System can retain stored channel data indefinitely unless manually deleted outside the system.

### Question Detection & Intake

- FR11: Busy Community Member can ask a question by **mentioning the bot** in a channel message.
- FR12: Busy Community Member can ask a question by **replying to the bot** in a channel thread.
- FR13: System can ignore messages that are neither a bot mention nor a reply-to-bot (not treated as a question).
- FR14: Busy Community Member can request usage instructions via **`/help`**.

### Answer Generation & Presentation

- FR15: System can respond to a question with a **threaded reply** in the same channel.
- FR16: System can format answers using **Telegram MarkdownV2**.
- FR17: System can include **Top 3** recommendations in an answer when applicable.
- FR18: System can include **citations** for answer content (Telegram message link when possible; fallback citation otherwise).
- FR19: System can include **message dates** alongside citations.
- FR20: System can include an **“as-of cutoff” timestamp (IST)** in every answer (e.g., “Based on messages up to … (IST)”).
- FR21: System can extract and display contact details when they are present in source messages.
- FR22: System can avoid fabricating contact details when none exist in sources.
- FR23: System can handle “conflicting recommendations” by presenting Top 3 while explicitly reflecting disagreement and supporting evidence.

### Recommendation Exploration (“More recommendations”)

- FR24: Busy Community Member can request more recommendations via an inline **“More recommendations”** button.
- FR25: System can return the **next 3** distinct recommendations per click, up to **12 distinct** total for the same question context.
- FR26: System can ensure “More recommendations” results preserve citations + dates + cutoff timestamp formatting.
- FR27: System can ensure “More recommendations” does **not** consume daily quota.

### Quota Management (Per Channel)

- FR28: System can enforce a **per-channel daily question quota** (default 50/day/channel).
- FR29: System can reset a channel’s quota at **midnight India time**.
- FR30: System can inform users when a channel’s daily quota is exhausted and refuse additional questions until reset.

### Feedback Capture

- FR31: Busy Community Member can provide feedback on answers via **👍/👎 reactions** on the bot’s answer message.
- FR32: System can record feedback events for later analysis.

### Safety & Guardrails

- FR33: System can evaluate user queries against safety policies and refuse to answer when required.
- FR34: System can quarantine safety-flagged ingested content so it is excluded from normal answering.

### Bot Membership, Permissions, and Audit Events

- FR35: System can detect bot removal from a channel when Telegram provides such signals.
- FR36: System can detect bot permission changes when Telegram provides such signals.
- FR37: System can create an audit event when the bot is removed from a channel.
- FR38: System can create an audit event when the bot’s permissions change in a channel.
- FR39: System can stop ingesting from a channel after bot removal (or adjust behavior appropriately after permission loss).

### System Operator Messaging (Out-of-Band)

- FR40: System Operator can send a message to a specific onboarded channel outside the normal Q&A flow.
- FR41: System Operator can broadcast a message to all onboarded channels outside the normal Q&A flow.
- FR42: System Operator can trigger out-of-band messaging via an ops **CLI**.
- FR43: System Operator can trigger out-of-band messaging via an **internal-only HTTP endpoint**.

### Failure Handling

- FR44: System can notify the user when it cannot produce an answer and ask them to try again later.

## Non-Functional Requirements

### Performance

- **Latency (MVP):** Average end-to-end answer latency is **< 5 seconds**.
- **Tail latency (MVP):** P95 end-to-end answer latency is **≤ 15 seconds**.
- **User feedback during processing:** The bot must provide immediate feedback via **Telegram “typing…”** while processing.

### Reliability

- No explicit uptime % target for MVP, but the system should degrade gracefully:
  - If an answer cannot be produced, respond with a clear fallback (“try again later”) rather than failing silently.

### Security

- **Channel isolation:** The system must prevent **cross-channel leakage** (answers must only use evidence from the channel where the question was asked).
- **Secrets handling:** Provider API keys/secrets must not be exposed in logs or bot responses.
- **Internal operator endpoint:** Network-restricted access is sufficient for MVP (no additional auth required).

### Scalability

- **Channel scale (MVP):** Support up to **5 onboarded channels** per system instance with acceptable performance (per the latency targets).

### Integration

- Telegram integration must be robust under normal API/network variability (retries/backoff as appropriate), without compromising channel isolation.

### Observability

- The system must emit **structured logs** and include **correlation IDs** to support troubleshooting and auditing (especially for “bot not responding”, quota enforcement, and channel membership/permission changes).

