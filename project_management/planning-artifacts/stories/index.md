# tgbot Stories (Materialized from epics.md)

Source: `project_management/planning-artifacts/epics.md`

## Epic 1: Onboard a community channel and make the bot usable

- **Story 1.1**: [Set up initial project from the selected starter template](project_management/planning-artifacts/stories/epic-01/story-01-01-set-up-initial-project-from-the-selected-starter-template.md)
- **Story 1.2**: [Register a channel (ops CLI) with per-channel disclaimer](project_management/planning-artifacts/stories/epic-01/story-01-02-register-a-channel-ops-cli-with-per-channel-disclaimer.md)
- **Story 1.3**: [`/help` returns usage instructions + channel disclaimer (threaded)](project_management/planning-artifacts/stories/epic-01/story-01-03-help-returns-usage-instructions-channel-disclaimer-threaded.md)
- **Story 1.4**: [Resolve incoming updates to a known channel record](project_management/planning-artifacts/stories/epic-01/story-01-04-resolve-incoming-updates-to-a-known-channel-record.md)
- **Story 1.5**: [Create minimal persistence for channels and audit events](project_management/planning-artifacts/stories/epic-01/story-01-05-create-minimal-persistence-for-channels-and-audit-events.md)

## Epic 2: Capture and maintain the community knowledge base (ingest + backfill + lifecycle)

- **Story 2.1**: [Normalize Telegram updates into a versioned event envelope and enqueue them durably](project_management/planning-artifacts/stories/epic-02/story-02-01-normalize-telegram-updates-into-a-versioned-event-envelope-and-enqueue-them-durably.md)
- **Story 2.2**: [Consolidate queued envelopes into immutable raw-lake JSONL windows + manifest](project_management/planning-artifacts/stories/epic-02/story-02-02-consolidate-queued-envelopes-into-immutable-raw-lake-jsonl-windows-manifest.md)
- **Story 2.3**: [Process lake window files into “latest message state” with edits and tombstones](project_management/planning-artifacts/stories/epic-02/story-02-03-process-lake-window-files-into-latest-message-state-with-edits-and-tombstones.md)
- **Story 2.4**: [Implement userbot-based historical backfill and cursoring](project_management/planning-artifacts/stories/epic-02/story-02-04-implement-userbot-based-historical-backfill-and-cursoring.md)
- **Story 2.5**: [Ensure retention policy and manual deletion posture are documented and enforced](project_management/planning-artifacts/stories/epic-02/story-02-05-ensure-retention-policy-and-manual-deletion-posture-are-documented-and-enforced.md)

## Epic 3: Ask questions in-channel and get evidence-backed answers (Top-3)

- **Story 3.1**: [Detect questions (bot mention / reply-to-bot) and ignore other messages](project_management/planning-artifacts/stories/epic-03/story-03-01-detect-questions-bot-mention-reply-to-bot-and-ignore-other-messages.md)
- **Story 3.2**: [Send “typing…” immediately and reply in-thread with a safe fallback on failure](project_management/planning-artifacts/stories/epic-03/story-03-02-send-typing-immediately-and-reply-in-thread-with-a-safe-fallback-on-failure.md)
- **Story 3.3**: [Enforce strict channel-scoped retrieval (no cross-channel leakage)](project_management/planning-artifacts/stories/epic-03/story-03-03-enforce-strict-channel-scoped-retrieval-no-cross-channel-leakage.md)
- **Story 3.4**: [Retrieve, rank, and return Top 3 distinct recommendations with citations and dates](project_management/planning-artifacts/stories/epic-03/story-03-04-retrieve-rank-and-return-top-3-distinct-recommendations-with-citations-and-dates.md)
- **Story 3.5**: [Always include the cutoff timestamp line (IST) in answers](project_management/planning-artifacts/stories/epic-03/story-03-05-always-include-the-cutoff-timestamp-line-ist-in-answers.md)
- **Story 3.6**: [Extract and display contact details only when present in evidence](project_management/planning-artifacts/stories/epic-03/story-03-06-extract-and-display-contact-details-only-when-present-in-evidence.md)
- **Story 3.7**: [Format answers in Telegram MarkdownV2 safely](project_management/planning-artifacts/stories/epic-03/story-03-07-format-answers-in-telegram-markdownv2-safely.md)
- **Story 3.8**: [Handle conflicting recommendations neutrally with evidence](project_management/planning-artifacts/stories/epic-03/story-03-08-handle-conflicting-recommendations-neutrally-with-evidence.md)

## Epic 4: Explore more results and enforce per-channel daily quota

- **Story 4.1**: [Enforce per-channel daily question quota with IST midnight reset](project_management/planning-artifacts/stories/epic-04/story-04-01-enforce-per-channel-daily-question-quota-with-ist-midnight-reset.md)
- **Story 4.2**: [Provide “More recommendations” button that paginates +3 up to 12 distinct](project_management/planning-artifacts/stories/epic-04/story-04-02-provide-more-recommendations-button-that-paginates-3-up-to-12-distinct.md)

## Epic 5: Safety and feedback loop

- **Story 5.1**: [Query safety gate (refuse flagged queries with a supportive response)](project_management/planning-artifacts/stories/epic-05/story-05-01-query-safety-gate-refuse-flagged-queries-with-a-supportive-response.md)
- **Story 5.2**: [Quarantine unsafe ingested content and hard-filter it from answering](project_management/planning-artifacts/stories/epic-05/story-05-02-quarantine-unsafe-ingested-content-and-hard-filter-it-from-answering.md)
- **Story 5.3**: [Capture 👍/👎 feedback on bot answers](project_management/planning-artifacts/stories/epic-05/story-05-03-capture-feedback-on-bot-answers.md)

## Epic 6: Operate and troubleshoot the bot (membership/permissions, audit events, ops messaging)

- **Story 6.1**: [Detect bot removal/permission changes and emit audit events](project_management/planning-artifacts/stories/epic-06/story-06-01-detect-bot-removal-permission-changes-and-emit-audit-events.md)
- **Story 6.2**: [Ops CLI to send a message to one channel or broadcast to all channels](project_management/planning-artifacts/stories/epic-06/story-06-02-ops-cli-to-send-a-message-to-one-channel-or-broadcast-to-all-channels.md)
- **Story 6.3**: [Internal-only HTTP endpoint for ops messaging](project_management/planning-artifacts/stories/epic-06/story-06-03-internal-only-http-endpoint-for-ops-messaging.md)

