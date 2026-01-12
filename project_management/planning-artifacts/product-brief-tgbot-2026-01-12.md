---
stepsCompleted: [1, 2, 3, 4, 5]
inputDocuments: []
date: 2026-01-12
author: Kuldeep
---

# Product Brief: tgbot

<!-- Content will be appended sequentially through collaborative workflow steps -->

## Executive Summary

tgbot helps gated communities make sense of high-volume, unstructured Telegram conversations by turning past chat history into fast, consolidated answers via simple bot interactions. Instead of relying on Telegram search or scrolling through 200–500 daily messages, members can ask questions like “recommended electrician?” or “pet rules in practice?” and receive a synthesized response grounded in prior community discussions. The MVP focuses on Telegram and supports multiple channels per community (e.g., owners + residents), with a clear path to expand to WhatsApp and email in later phases.

A key design principle is trust: responses should include a recency-weighted confidence signal and allow users to trace answers back to the original messages.

---

## Core Vision

### Problem Statement

In Telegram-based communities, valuable information (trusted service contacts, nuanced do/don’t guidance, and first-hand experiences) gets buried under daily message volume and concurrent conversations. Members cannot reliably retrieve or consolidate what the community already knows when they need it, especially across multiple channels.

### Problem Impact

- Important recommendations and context are lost in noise, forcing repeated questions and duplicated effort.
- New members face a steep ramp-up and miss practical, experience-based guidance that matters more than high-level rules.
- Telegram search returns fragments, not consolidated, decision-ready answers (e.g., “best electrician + why + evidence”).

### Why Existing Solutions Fall Short

- Search provides isolated messages without synthesis, ranking, or confidence.
- Pins/announcements capture official guidelines but miss lived experiences and practical trade-offs.
- Manual reading doesn’t scale at 200–500 messages/day.
- Knowledge is split across channels (owners vs residents), making consolidation even harder.

### Proposed Solution

A Telegram bot that indexes a community’s Telegram channels and provides conversational Q&A and summaries on demand. Members ask natural-language questions and receive consolidated answers reflecting prior recommendations and experiences. By default, answers prioritize the most recent relevant discussions and include links back to the original messages for verification.

The bot responds only within the channel context (no DMs), keeping interactions lightweight and familiar for community members.

### Key Differentiators

- Community knowledge consolidation (synthesis) rather than simple retrieval.
- Trust-first UX with:
  - Recency-weighted “confidence” signals (recent recommendations prioritized)
  - Traceability via links back to source messages
- Default response format optimized for action:
  - A concise summary plus linked supporting messages
- Pragmatic language approach:
  - English-first; Hinglish support is a nice-to-have if complexity is manageable
- Roadmap-ready for multi-channel ingestion beyond Telegram (WhatsApp/email) after MVP validation

---

## Target Users

### Primary Users

**Core Persona: “The Busy Community Member” (owner/resident/admin mix)**  
A member of a gated-community ecosystem who relies on Telegram channels for day-to-day coordination and information. They don’t have time to read 200–500 daily messages and need quick, trustworthy, experience-based answers.

**Goals**
- Find the “best next action” fast (e.g., who to call for a specific repair/service).
- Use community-first-hand experiences rather than generic guidelines.

**How they experience the problem today**
- Information is buried across multiple community channels (owners vs residents).
- Search returns fragments; they still can’t confidently decide or compare.
- The same questions get asked repeatedly by different people.

**Success for them (“this is exactly what I needed”)**
- Bot returns **Top 3** relevant recommendations with:
  - **Contact details** (when present in chat)
  - **Evidence links back to source messages**
  - **Date shown** so they understand recency
- No need for pricing/availability details (out of scope).

**Representative example**
- Query: “LG top load washing machine repair”
- Expected ranking logic: (1) LG top-load specific, then (2) LG (any), then (3) top-load (any brand), then broader washing-machine recommendations.

### Secondary Users

N/A (MVP focuses on one core persona; any member can benefit similarly.)

### User Journey

- **Discovery**: Bot is added to the community channel(s) and **pinned**, making it visible as the go-to “ask here” entry point.
- **Onboarding**: User sees pinned bot and tries a natural-language query.
- **Core Usage**: User types a natural language question; bot responds with top recommendations + evidence links + dates.
- **Success Moment**: User quickly finds a relevant, recent, traceable recommendation without scrolling/searching.
- **Long-term**: As more members use it, repeated questions reduce and the bot becomes the default way to retrieve community knowledge.

---

## Success Metrics

### User Success Metrics

- **Time-to-answer (performance)**: Users receive **Top 3** relevant answers in **under 3 seconds on average**.
- **Helpfulness signal (quality proxy)**: After each response, bot asks “Was this helpful?” and users can react with **👍 / 👎**.
  - **Success threshold (first 3 months)**: **≥ 40% 👍** among responses that receive a rating (acknowledging many users may not rate, and early data may fluctuate).

### Business Objectives

- **3-month objective (adoption)**: Reach **10–15 queries/day per community**.
- **12-month objective (growth)**: Onboard **4 communities**.
  - Assumption/definition of target community scale: ~**1000 users/community**, ~**200 messages/day** volume/community.

### Key Performance Indicators

- **Avg response latency**: < 3 seconds (average).
- **Queries/day per community**: Target 10–15 by month 3.
- **Rated response helpfulness (👍 rate)**: ≥ 40% in first 3 months (among rated responses).
- **Communities onboarded**: 4 by month 12 (with target community scale as noted above).

---

## MVP Scope

### Core Features

- **Telegram ingestion (multi-channel per community)**: Connect **1 community** with **multiple Telegram channels** (e.g., owners + residents) and continuously capture new messages.
- **Index + retrieval over chat history**: Store messages in a searchable/indexed form so older recommendations can be found reliably.
- **Natural-language Q&A in-channel**: Users ask a question in the channel; bot replies in the **same channel** (no DMs).
- **Top-3 ranked recommendations**: For “find a service/vendor” queries, return **top 3** results ranked by **relevance + recency** (e.g., LG top-load > LG any > top-load any).
- **Evidence + traceability**: Each recommendation includes **links to original messages** and shows **date** of supporting messages.
- **Contact extraction (when present)**: If phone/contact details are present in chat, include them in the recommendations.
- **Feedback capture**: After each answer, prompt “Was this helpful?” and capture **👍 / 👎**.

### Out of Scope for MVP

- **Any integrations beyond Telegram** (no WhatsApp, no email, etc.).
- **Any external portal/web UI** (Telegram-only UX).
- **DM support** (bot will not answer in 1:1 chat).
- **Pricing/availability workflows** (scheduling, negotiation, live availability, etc.).
- **Admin/mod tooling** (dashboards, moderation controls, approval flows, role-based access).
- **Advanced multilingual support** (Hinglish/Hindi-first) if it materially complicates MVP delivery.

### MVP Success Criteria

MVP is considered successful (and a “go” to scale) if it meets the already-defined metrics:

- **Avg response time**: Top-3 answers returned in **< 3 seconds (average)**.
- **Adoption**: **10–15 queries/day per community** by month 3.
- **Quality proxy**: **≥ 40% 👍** among rated responses in the first 3 months (acknowledging many users may not rate).

### Future Vision

- **Next (post-MVP)**: Improve language support, aiming for **Hinglish** support if feasible without degrading quality/performance.
- **Then**: Expand ingestion beyond Telegram, starting with **WhatsApp**.
- Longer-term: Support additional channels (e.g., email) and richer community knowledge workflows as the product proves value.

