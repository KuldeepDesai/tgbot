---
stepsCompleted: [1, 2]
inputDocuments: []
session_topic: 'Cost-optimized Telegram ingestion + processing pipeline for developers (1000s msgs/day) into a manageable platform'
session_goals: 'Define an MVP solution that is feasible and cost-optimized; supports pipeline-style processing, natural-language interaction, safety/ethics filtering + guardrails, and full reprocessing/replay capability'
selected_approach: 'ai-recommended'
techniques_used:
  - First Principles Thinking
  - Resource Constraints
  - Role Playing (optional if time allows)
ideas_generated: 10
context_file: '/Users/Kuldeep_Desai/workspace/exp/tgbot/_bmad/bmm/data/project-context-template.md'
---

# Brainstorming Session Results

**Facilitator:** Kuldeep
**Date:** 2026-01-12

## Session Overview

**Topic:** Cost-optimized Telegram ingestion + processing pipeline for developers (1000s msgs/day) into a manageable platform
**Goals:** Define an MVP solution that is feasible and cost-optimized; supports pipeline-style processing, natural-language interaction, safety/ethics filtering + guardrails, and full reprocessing/replay capability

### Context Guidance

This session will explore:

- User problems and pain points for developers interacting with Telegram
- Feature ideas and capabilities for ingest + manage + query messages
- Technical approaches for a pipeline architecture (ingestion, processing, storage, serving)
- UX for the “manageable platform” and bot interaction flows
- Business/value framing for an MVP that minimizes cost
- Market differentiation and success metrics
- Technical risks (scale, reliability, privacy/security) and mitigation

### Session Setup

- **Non-goals for now**: Prematurely locking into a single architecture before exploring multiple cost/complexity tradeoffs.
- **Hard constraints**: MVP should be cost-optimized; must support “replay/reprocess everything”; must apply safety/ethics filtering and guardrails in responses; must support natural-language interaction with the bot.

## Technique Selection

**Approach:** AI-Recommended Techniques
**Analysis Context:** Cost-optimized Telegram ingestion + processing pipeline with focus on feasibility, low MVP cost, replay/reprocess, natural-language bot interaction, and safety/ethics guardrails.

**Recommended Techniques:**

- **First Principles Thinking**: Quickly defines the minimum viable pipeline “truths” and eliminates default assumptions (e.g., what “replay” must guarantee, what must be stored, where safety gates belong).
- **Resource Constraints**: Forces cost-first architecture choices (cheap deployment, batch vs streaming, minimal always-on services, controlling LLM usage).
- **Role Playing (optional if time allows)**: Stress-tests the design from Developer, End-User, Trust & Safety, and Compliance perspectives to shape safe defaults (e.g., self-harm content handling should be *escalate/quarantine with safe responses*, not silent discard).

**Session Timebox:** 15 minutes preferred (extendable to 30 minutes)

## Technique Execution Results

### Technique 1: First Principles Thinking

#### Non-negotiable “must be true” MVP requirements (initial set)

- **Safety gate (self-harm / abuse):** If a message triggers self-harm or abusive/harassing signals, the bot must not treat it as normal Q&A content and must follow a safe policy.
- **In-channel NL Q&A + performance:** For a natural-language question posted in a community Telegram channel, the bot must respond in the same channel with Top 3 ranked results in < 3 seconds on average.
- **Traceability + trust signal:** Every recommendation must include links back to original source messages and show dates (recency) so users can verify evidence.

#### Safety policy decision (quarantine semantics)

- **Decision:** Safety-triggering content will be **quarantined** (excluded from normal Q&A synthesis/indexing) with sufficient metadata to support audit + enforcement.
- **Metadata to retain (MVP):** Telegram `user_id`, `chat_id`, `message_id`, timestamp, classifier labels/scores, and a minimal redacted excerpt (or encrypted full text) to enable review while limiting exposure.
- **User-facing response policy:** For safety triggers (including self-harm), the bot should respond with a **supportive safe response** (never punitive).
- **Enforcement policy:** **Bans are not automatic**. Quarantined content enables **flagging** and **manual moderation actions** (e.g., temporary block or ban) when appropriate.
- **Vector indexing:** Quarantined content is **included in the vector index with metadata** (e.g., `quarantined=true`, labels/scores) so retrieval can explicitly filter it out (default) while still supporting audits/analysis.
- **Response policy:** For normal user queries, responses must **hard-filter out** `quarantined=true` content (quarantined messages are never used as evidence/citations in answers).
- **Query safety gate:** If the **user’s query** is flagged (e.g., self-harm, harassment), the bot must **refuse and provide a supportive safe response**, and **skip retrieval/synthesis entirely**.

### Technique 2: Resource Constraints (budget-first)

#### Deep dive: (1) Evidence-First MVP + (2) SQLite-only backend

**Goal:** Achieve “Top-3 answers with receipts” at <$10/mo by default, while preserving a path to richer synthesis later.

**Proposed MVP architecture (minimal moving parts):**

- **Telegram ingestion**: Receive updates (prefer webhook if hosting supports it; polling as fallback).
- **Safety gate (cheap first)**: Classify messages for safety; quarantine flagged content (excluded from Q&A/indexing) + reply with supportive safe response.
- **Storage**: SQLite for everything (single file DB) + optional daily DB backup.
- **Retrieval**: SQLite FTS (full-text search) over message text + light metadata filters (channel, date window).
- **Ranking**: Weighted scoring: relevance (FTS rank) + recency boost + (optional) “contact present” boost for vendor queries.
- **Answer format**: Standard “Top 3” with:
  - short bullet summary per item
  - message link(s) + date(s)
  - extracted phone/contact when present
  - confidence signal (simple recency + evidence count heuristic)
- **Caching**: Cache common queries + invalidate when new relevant messages arrive.
- **LLM usage (optional / on-demand)**: Only when retrieval confidence is low or user explicitly asks for a synthesized summary; always include citations.

**SQLite MVP data model (sketch):**

- `messages(id, chat_id, channel_id, message_id, user_id, ts, text, has_contact, permalink, safety_label, safety_score, quarantined)`
- `messages_fts(text, message_rowid)` (FTS virtual table linked to `messages`)
- `answers_cache(chat_id, normalized_query, answer_json, created_ts, max_source_ts)`
- `moderation_queue(id, chat_id, message_id, user_id, ts, label, score, status, notes)`

**How this stays cheap:**

- No always-on vector DB.
- No mandatory embedding generation.
- No heavy summarization jobs unless explicitly invoked.
- Single DB file keeps ops overhead near-zero.

**Key tradeoffs (explicit):**

- FTS relevance is not as semantically strong as embeddings → mitigated by a tight answer format + recency + user feedback loop (👍/👎).
- Multi-channel + scaling beyond a few communities may outgrow SQLite → acceptable for MVP; migrate later once usage proves value.

#### Decision: synthesis must be default (cost-optimized implementation)

- **Decision:** Answers should be **synthesized by default** (not just top snippets), while still including **citations (message links + dates)**.
- **Cost guardrails:** Synthesis runs only over a **small retrieved evidence set** (e.g., top-K messages + limited time window), with strict token budgets and aggressive caching (per community + normalized query).
- **Fallback behavior:** If evidence is weak/insufficient, respond with a synthesized “what we found / what we don’t know” plus the best available citations, rather than hallucinating.
- **Execution decision:** Use **external APIs** for synthesis (and ideally intent/safety classification) to offload compute/ops, while keeping the core pipeline thin.

#### Update: evaluate Vector + (optional) Graph before locking storage choice

- **Note:** SQLite is a **candidate** for MVP simplicity, but we will also evaluate **Vector DB** (for semantic retrieval) and **Graph DB** (for relationship-heavy queries) because the core requirement is making sense of unstructured chat via natural language.
- **Likely cost-optimized shape:** **Hybrid** — keep raw messages in a cheap store (SQLite/Postgres) while using a **managed vector index** (or externally hosted embeddings + search) for semantic retrieval; add a graph layer only if relationship queries become core.

#### Combined approach (Vector + Relationship filtering) to minimize LLM context

- **Core insight:** We should use **both simultaneously** so we don’t over-fetch from vector search and dump too much into the LLM.
- **Retrieval pipeline (MVP):**
  1. **Intent + constraint extraction (cheap):** detect query intent (e.g., vendor recommendation vs rules vs summary), and extract constraints (channel scope, time window, entity type).
  2. **Vector retrieval (broad recall):** pull top-K candidate messages/chunks semantically (K small, e.g., 50–200).
  3. **Relationship/graph filter (precision):** use a lightweight graph layer to:
     - dedupe by **entity/vendor**
     - prefer **recent** mentions
     - weight by **#independent recommenders**
     - enforce **channel** / **community** boundaries
     - collapse many messages into **Top-N entities** with a few best citations each
  4. **LLM synthesis (default):** synthesize over the reduced “evidence pack” (e.g., 10–30 messages max), always outputting citations.
- **Implementation note:** For MVP, the “graph” does not need a dedicated Graph DB — it can be represented as **edge tables** (e.g., `message -> entity`, `user -> entity`, `entity -> category`) in the same DB, with a later migration to a graph database only if needed.

#### Relationship priority (graph MVP)

- **Primary (A): Entity/vendor centric**: `message -> entity/vendor/service -> category` to dedupe and rank vendors/services with strong citations.
- **Secondary (B): User trust centric**: weight entities by **# unique recommenders** (MVP: **unique only**, no role boosts), to avoid over-counting one loud participant and to improve ranking quality.

#### MVP graph representation (as DB edge tables, not necessarily a dedicated Graph DB)

- `entities(entity_id, normalized_name, entity_type, category, created_ts)`
- `message_entities(message_id, entity_id, sentiment, extracted_contact, extracted_context)`
- `entity_recommenders(entity_id, user_id, first_seen_ts, last_seen_ts)` (can be derived from `message_entities`)

#### Entity ranking (simple, explainable scoring)

- **Candidate set**: Vector top-K messages/chunks for the query.
- **Aggregate to entities**: Map candidate messages → entities; keep top citations per entity.
- **Score example (MVP):**
  - \(score(entity) = w_s \cdot max(similarity) + w_r \cdot recency\_boost + w_u \cdot log(1 + unique\_recommenders)\)
  - Ensure **unique recommenders** counts distinct `user_id` values (no role boosts).

#### Vector indexing decision (MVP)

- **Decision:** Embed **chunks** (conversation chunks / rolling summaries) instead of every raw message to reduce cost and improve context quality.
- **Citation preservation:** Each chunk should retain the list of underlying `message_id` links so the bot can always cite original messages/dates.

#### Chunking strategy decision (MVP)

- **Decision:** Use **time windows** for chunk formation.
- **Default window:** Consolidate messages every **4 hours** (configurable).
- **Transparency requirement:** Every answer must disclose the **cut-off time** (e.g., “Based on messages up to 2026-01-12 16:00”) so users understand recency boundaries.
- **Cut-off scope:** **Per-community** (single cut-off across all channels for a community), so answers spanning channels share a consistent freshness boundary.

#### Trust signal decision (Telegram-native UX)

- **Decision:** No explicit “confidence” indicator in MVP (to keep responses feeling native to Telegram).
- **Trust signals instead:** citations (message links + dates) + per-community cutoff time.
- **Feedback collection (MVP):** Use Telegram-native **👍/👎 reactions** on the bot’s answer message (no follow-up prompt).

#### Access + scope decision (MVP)

- **Decision:** Retrieval/synthesis should be **query-scoped** to respect channel access boundaries.
- **Default scope:** Only use sources from the **current channel** where the question was asked (and any configured sub-scopes that are guaranteed accessible to that user).
- **Rationale:** Not all users have access to all channels; the bot must not leak information across private channels via synthesis.
- **MVP rule:** **Always query-scoped** (current-channel only). Cross-channel search (even if explicitly requested) is a **post-MVP enhancement** gated by explicit admin configuration + robust permission checks.

#### SaaS Vector DB free-tier candidates (to validate before committing)

- **Upstash Vector**: Official pricing page indicates a **free plan** with a daily **10,000 query/update** limit (serverless), which can fit early MVP workloads. See `https://upstash.com/pricing/vector`.
- **Weaviate Cloud**: Official pricing page indicates a **14-day free trial** (not a permanent free tier). See `https://weaviate.io/pricing`.
- **Vectroid**: Vendor claims a free allocation of **100GB index storage**, **10M writes/month**, **1M queries/month** (verify fit + maturity). See `https://www.vectroid.com/blog/100gb-of-vector-indexes-free`.

#### Vector DB decision (MVP) + portability requirement

- **Decision:** Use **Upstash Vector** for MVP (free tier, serverless).
- **Portability requirement:** Design the system **DB-agnostic** by isolating vector operations behind a small interface (e.g., `VectorStore` with `upsertChunks()`, `queryChunks()`, `deleteByChannel()`, `deleteByCommunity()`, `health()`), so we can later swap to another vector backend (pgvector/Qdrant/Pinecone/etc.) with minimal changes.

#### Primary data store decision (MVP)

- **Decision:** Use **managed Postgres** for raw messages + metadata + quarantine/moderation + entity edges to minimize ops.
- **Cost goal:** Prefer a provider with a **free tier** for MVP; validate limits (storage, compute/sleep, connection caps) before committing.

#### Data lake (raw archive) decision (MVP — mandatory)

- **Decision:** A “raw data lake” (object storage; S3/GCS/Azure/MinIO-equivalent) is **mandatory** in MVP to keep ingestion isolated from processing and to make rebuilds/vendor swaps practical.
- **Provider (MVP default):** Use **Azure Blob Storage**, but keep it **configurable/pluggable** via a storage interface (e.g., `ObjectStore` / `DataLakeStore`) so we can swap to S3/GCS/MinIO later.
- **Role separation:**
  - **Lake = immutable raw archive + replay source**: write append-only 4-hour dumps per channel (e.g., JSONL/Parquet) + manifests; store attachment binaries later (multimodal).
  - **Postgres = operational state + indexes**: cursors/watermarks, idempotency, community↔channel mapping, audit/cost events, feature flags, entity edges.
  - **Vector store = retrieval index**: embeddings over 4-hour chunks; pluggable backend.
- **Pipeline shape:** ingestion writes to lake + minimal Postgres records; batch processor reads from lake sequentially and produces derived artifacts (Postgres tables, vector upserts).
- **Enterprise benefit:** Supports future WhatsApp/email ingestion and multimodal processing without schema churn; enables fast rebuilds without re-fetching from upstream providers.

#### Data lake raw format decision (MVP)

- **Decision:** Store 4-hour per-channel dumps as **JSONL** (simple + debuggable).

#### Managed Postgres free-tier candidates (MVP)

- **Neon** (serverless Postgres): `https://neon.tech/pricing`
- **Supabase** (Postgres + auth/storage optional): `https://supabase.com/pricing`
- **Aiven** (managed Postgres free offering): `https://aiven.io/free-postgresql-database`
- **AWS RDS free tier** (12-month free for new AWS accounts): `https://aws.amazon.com/rds/free/`

_Note: provider free-tier limits change; confirm exact quotas before wiring credentials into the MVP._

#### Managed Postgres vendor decision (MVP) + portability requirement

- **Decision:** Use **Aiven Postgres** for MVP.
- **Portability requirement:** Treat Postgres as a **pluggable dependency**:
  - Use a standard `DATABASE_URL` connection string and stick to portable SQL + migrations.
  - Avoid vendor-specific extensions/features unless guarded behind optional capabilities.
  - Isolate DB access behind a small data-access layer (e.g., repositories) so swapping vendors is just changing `DATABASE_URL`.

#### Ingestion + batching decision (MVP)

- **Decision:** Use Telegram **webhooks** for low-latency collection of raw message events, but make ingestion **Logstash-like**:
  - webhook accepts events and writes them to a **dedicated event buffer** (not Postgres)
  - a 4-hour consolidator writes buffered events into immutable **raw lake files**
  - downstream processing workers ingest **files** into Postgres + vector store
- **Cost principle:** Avoid always-on compute for heavy processing; only the webhook endpoint and managed event buffer must be reachable, and expensive work is timeboxed/parallelized.

#### Logstash-like ingestion workflow (MVP)

- **Stage 0: Webhook event capture (thin)**
  - Bot receives updates (message/new, edit, delete, reactions)
  - Writes the raw update + minimal routing metadata to an **event buffer** (Azure-managed), returning quickly.
  - **Event buffer choice (MVP):** **Azure Storage Queue** (cheap/simplest).
- **Stage 1: 4-hour file consolidation → raw lake**
  - A scheduled consolidator drains/reads events for each channel window and writes **JSONL** to Azure Blob:
    - `raw/{community_id}/{channel_id}/YYYY/MM/DD/HH00-<HH00+4h>.jsonl`
  - Writes a small manifest (counts, min/max message_id, time range, schema version).
  - **Ordering (MVP):** Best-effort ordering is acceptable; downstream processors should be idempotent and apply a “latest version wins” rule for edits/deletes/reactions.
- **Stage 2: Parallel file ingestion workers (fan-out)**
  - Multiple workers process multiple window files simultaneously (bounded concurrency):
    - normalize + apply edits/deletes
    - safety labeling/quarantine metadata
    - entity/rule-topic extraction + edge tables
    - chunk embedding → Upstash Vector upsert
    - audit + cost events, and daily rollups
  - Idempotency: workers claim a file (lease/lock), write a processing status row, and are safe to retry.

#### Multimodal ingestion (MVP)

- **Reality:** Telegram messages may include photos, videos, voice notes, files/PDFs, stickers, locations, and forwarded messages.
- **Ingestion principle:** Always ingest **message metadata + pointers** (file_id, mime type, size) into Postgres so replay/rebuild works, even if we don’t process content immediately.
- **Metadata emphasis (MVP):** Store **filenames** (when present) and other attachment metadata because filenames can carry semantic hints even without OCR/transcription.
- **Processing tiers (cost-aware):**
  - **Tier 0 (store only):** keep metadata + download URL/file_id, no transcription/OCR (cheapest).
  - **Tier 1 (text extraction):** OCR images and extract text from PDFs; speech-to-text for voice notes (higher cost).
  - **Tier 2 (multimodal embeddings):** generate embeddings from extracted text (still “text-only embedding”), and optionally store thumbnails/snippets for citations.
- **Chunking impact:** 4-hour channel windows should include extracted text (if enabled) so the chunk summary/embedding captures multimodal knowledge.

#### Attachment citation + ranking rule (MVP)

- **Citation:** It’s acceptable to cite attachments by **filename + date + message link** even if the contents weren’t extracted (e.g., “Referenced file: `<filename>` (posted on `<date>`)”).
- **Ranking:** Always prefer **known text content** over **unknown attachment-only content**. Attachment-only messages should be down-ranked and only used when no better textual evidence exists.
- **Edge case behavior:** If top matches are mostly attachments, the bot should still respond with the best available info and explicitly disclose: **“I can’t read files yet in MVP.”**

#### Telegram message lifecycle behaviors (MVP)

- **Edits:** Treat message edits as new versions of the same message_id; keep latest text for retrieval/synthesis and keep a minimal audit trail if needed.
- **Deletes:** Keep full deleted content in the DB for rebuild/debug purposes, but **exclude deleted messages from retrieval/synthesis/citations** going forward (so we don’t cite content users removed). Maintain a tombstone flag/status for idempotency/replay bookkeeping.

#### Reactions / upvotes signal (MVP)

- **Upvote definition:** Treat **any positive reaction emoji** (e.g., 👍/❤️/🔥) as an “upvote” signal (not just 👍).
- **Ranking impact:** Use upvotes as a **small tie-breaker boost** (should not outweigh recency or unique recommenders).
- **Anti-gaming:** Count **unique reactors** (distinct users who reacted) rather than raw reaction totals.
- **Scope:** Apply this boost across **all** retrieval/ranking surfaces (vendors/services and rule topics).

#### Explainability / “Why did you answer this?” (MVP)

- **UX concept:** After answering, support a follow-up user message like **“explain”** to show why the bot produced that answer.
- **Trigger decision (MVP):** Use an inline **“Explain” button** under the bot’s answer (Telegram inline keyboard / callback), not a typed command.
- **Visibility decision (MVP):** Explanation is posted **publicly in the channel** (same place as the answer).
- **Cost control:** Gate Explain behind a **per-community feature flag**. A community admin can disable it; once disabled, the Explain button is no longer shown on new bot responses for that community.
- **Default:** Explain is **disabled by default** for new communities; admins explicitly enable it when desired.

#### Audit / event logging (MVP, no dashboards yet)

- **Goal:** Capture enough structured events now so we can build post-MVP dashboards/analytics without losing history.
- **Approach:** Write append-only audit events to Postgres (e.g., `audit_events`) with:
  - `community_id`, `channel_id`, `user_id` (when applicable)
  - `event_type`, `event_ts`
  - `correlation_id` / `request_id` (tie webhook → batch run → answer)
  - `payload_json` (small, structured, versioned)
- **Examples of audit-able actions:**
  - ingestion events (message received/edited/deleted, attachment metadata seen)
  - batch pipeline runs (start/end, processed counts, cutoff advanced)
  - safety actions (query blocked, message quarantined)
  - answer served (intent, cutoff time, which sources were used, cache hit/miss)
  - explain clicked (enabled/disabled, reuse cache vs recompute)
  - feedback captured (👍/👎 reactions on bot answers)
  - admin config changes (e.g., enabling/disabling Explain)

- **MVP must-have event types:** **A+B+C+D+E**
  - **A** Ingestion lifecycle
  - **B** Batch runs
  - **C** Safety events
  - **D** Answer served (incl. source message IDs)
  - **E** Explain + feedback

- **Retention policy (MVP):** Keep audit events **forever**, but **cap payload sizes**:
  - store only small, versioned JSON fields + IDs/metrics (no large blobs)
  - reference heavy objects indirectly (e.g., `answer_id`, `message_ids[]`, `batch_run_id`)

#### Per-community cost accounting (MVP)

- **Goal:** Attribute “exact-ish” LLM spend to a **community**, so we can report cost per community and enforce budgets.
- **Approach:** For every external-model call (LLM synthesis, safety classifier, embeddings), write a **cost event** with:
  - `community_id`, `channel_id` (optional), `user_id` (optional)
  - `purpose` (e.g., `answer_synthesis`, `query_safety`, `chunk_embedding`)
  - `provider`, `model`, `pricing_version` (so historical totals remain stable even if prices change)
  - `input_tokens`, `output_tokens` (or equivalent units), `request_count`
  - `estimated_cost_usd` computed at write time (and stored), plus raw units for auditing
  - `correlation_id` tying it to the answer/query/batch run
- **Rollups (post-MVP):** Build daily/monthly aggregates per community from the immutable cost events.
- **Decision:** Store **per-call cost events + daily rollups** (daily aggregates) so “cost per community” is cheap to query even before dashboards.
- **Cost principle:** “Explain” should reuse the cached **evidence pack** from the original answer (no fresh retrieval) unless the cache is missing/expired.
- **Explain output (Telegram-native):**
  - Restate **cut-off time** and scope (current channel)
  - Show the **top evidence messages** used (links + dates), grouped by each Top-3 item or rule topic
  - Briefly list the top ranking signals (e.g., recency, # unique recommenders, unique reactors) as plain text bullets (no “confidence %”)

#### Replay / rebuild semantics (MVP + portability)

- **Default mode:** Incremental processing (each 4-hour run advances derived state from the last per-community cutoff).
- **Full rebuild requirement:** Must support a **full system rebuild from raw messages** for:
  - environment moves (dev → staging → prod)
  - switching vendors (vector DB, Postgres provider) or introducing a dedicated graph DB
- **Core design principle:** Treat raw ingested messages as the **source-of-truth event log**; everything else is **derived** and must be reproducible:
  - lake raw dumps (immutable) are the durable replay source
  - chunks/time windows
  - safety labels + quarantine records
  - entities/edges (vendors + rule topics, unique recommenders)
  - embeddings + vector index contents
  - caches
- **Implementation shape:** Provide an admin “rebuild” operation that can:
  - wipe derived tables + vector index namespaces/collections
  - re-run backfill in deterministic order
  - rebuild to the same per-community cutoff

#### Rebuild trigger (MVP)

- **Decision:** Full rebuild is triggered via an **ops-only CLI command** (not a bot command), to reduce blast radius and avoid accidental/abusive rebuilds.

#### Embedding cadence decision (MVP cost control)

- **Decision:** Generate embeddings for **every channel window** (each 4-hour chunk), not threshold-based, to keep retrieval completeness and predictability.

#### Graph/relationship layer scope decision (MVP)

- **Decision:** Relationship filtering must support **Vendors + Rules** (not vendors only).
- **Implication:** `entities.entity_type` should include at least: `vendor`, `service`, `rule_topic`.
- **Rule modeling (MVP):** Model rules as **canonical topics** (e.g., `pet_rules`, `parking_rules`) with citations to the best supporting messages; synthesize a user-facing topic summary but always link to evidence and show cutoff time.
- **Rules response UX (MVP):** Provide a **single best “current” summary** (not a debate view), backed by citations + cutoff time for transparency.

#### Privacy decision (MVP)

- **Decision:** No PII redaction in MVP; we can send **raw message text** to external APIs and make this explicit to users.

---

## Gap check against Product Brief (follow-ups before implementation)

Areas to explicitly decide before coding (to avoid churn):

- **Historical backfill**: MVP needs a way to ingest “past chat history” (Bot API limitations).
- **Permalinks**: How to generate stable message links in private groups/channels.
- **Admin onboarding/config**: How admins register a community + channels, and toggle flags (e.g., Explain) without a dashboard.
- **Cutoff semantics**: Per-community cutoff across multiple channels vs per-channel processing failures.

### Gap decision: Historical backfill (MVP)

- **Decision:** Use Telegram **Client API (userbot)** to backfill historical messages (to support “past chat history” in the product brief).
- **Notes:** This requires explicit operational safeguards (auth handling, rate limits, and clear user/admin consent) to avoid surprises.

#### Backfill + incremental fetching model (MVP draft)

- **Bot vs userbot roles:**
  - **Telegram Bot** (Bot API) is added to channels and records `channel_id`, `channel_name`, etc. and receives new messages going forward.
  - **Userbot** (Client API) is used for **history backfill** and for **incremental catch-up** beyond what Bot API can fetch.
- **Incremental cursor:** Telegram does not provide an HTTP-style ETag for chat history. For Client API, the practical cursor is:
  - **`last_seen_message_id` per channel** (preferred), or
  - **`last_seen_timestamp` per channel** (fallback/secondary).
  Message IDs are effectively monotonic within a chat and work well for paging history.
- **Backfill semantics:**
  - If `last_seen_message_id` is null → backfill “from beginning” (oldest available) up to present.
  - Otherwise → fetch messages with IDs greater than `last_seen_message_id` (or page forward using offset mechanics) and advance the cursor.

### Gap decision: Admin onboarding/config (MVP draft)

- **Channel registration:** When the bot is added to a channel, it writes channel metadata to Postgres.
- **Community mapping:** For MVP, a **system admin** (not Telegram channel admin) manages the mapping of **community ↔ channels** in the backend (manual ops process), since a community may include multiple channels.
- **Feature flags:** For MVP, community feature flags (e.g., enabling/disabling **Explain**) are managed by the **system admin only** (manual backend config change).

### Gap decision: Permalinks / citations (MVP)

- **Decision:** If clickable permalinks aren’t available (common in private groups/channels), MVP can fall back to:
  - `channel_name` + `date` + `message_id` (and optionally `sender`) as the citation.
- **When links are possible:** If we can form a Telegram link, include it (best effort).
- **Implementation note:** Store enough identifiers to support both:
  - public channel links (`t.me/<username>/<message_id>`) when a username exists
  - “private chat” style links (`t.me/c/<internal_chat_id>/<message_id>`) when applicable

### Gap decision: Per-community cutoff on partial failures + long backfills (MVP)

- **Decision:** **Advance per-community cutoff based on progress** (do not block on all channels succeeding).
- **Watermarks:**
  - Maintain a **per-channel cursor** (`last_seen_message_id` and/or `last_seen_ts`) for ingestion/backfill.
  - Derive a **per-community cutoff** as a best-effort “processed up to” watermark (and disclose it in answers), while allowing some channels to lag.
- **Timeboxing:** Each scheduled run is time-bounded (e.g., runs ~3 hours in a 4-hour cadence) and stops cleanly; next run resumes from stored cursors.
- **No competing threads:** Enforce **single-flight processing** per channel/community with a lock (e.g., Postgres advisory lock) so overlapping cron runs or backfills don’t compete.

#### Userbot setup (system-owned account) — operational notes

- **1) Create Telegram API credentials**
  - Go to `https://my.telegram.org` → **API development tools**
  - Create an app → collect **`api_id`** and **`api_hash`**
- **2) Create a userbot session**
  - Use a Telegram Client library (commonly **Telethon** or **Pyrogram**) to login once with:
    - the system-owned Telegram phone number
    - Telegram login code (and 2FA password if enabled)
  - Persist the resulting session securely (session file or session string).
- **3) Add the userbot account to target groups/channels**
  - The system admin adds this user account to the community’s groups/channels (read access required).
  - Ensure the account can read history (Telegram permissions vary by group/channel settings).
- **4) Wire secrets in backend**
  - Store `TELEGRAM_API_ID`, `TELEGRAM_API_HASH`, and the userbot session in secrets/env vars.
  - Treat these like production credentials (rotatable; never commit to git).
- **5) Backfill job**
  - Run an ops-only CLI that, per channel, pages history and updates `last_seen_message_id`.
  - Respect rate limits; implement retries + backoff.
