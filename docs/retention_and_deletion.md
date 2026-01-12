# Retention & Manual Deletion (MVP)

## Retention policy (MVP)

- The system **does not automatically purge** any stored channel data for MVP.
- All timestamps are stored in **UTC**; display in the bot is converted to **IST**.

## Manual deletion runbook (operator-driven)

If you receive a deletion request outside the system, you can remove a channel’s stored content with the steps below.

### 1) Identify the channel

- Find the row in Postgres `channels` by `telegram_chat_id` and note the internal `channel_id`.

### 2) Delete operational data from Postgres

In Postgres, delete rows for that `channel_id` (order below avoids FK issues):

- `audit_events` where `channel_id = <channel_id>`
- `messages` where `channel_id = <channel_id>`
- `answers` where `channel_id = <channel_id>`
- `channel_daily_quota` where `channel_id = <channel_id>`
- `channel_cursors` where `channel_id = <channel_id>`
- finally delete `channels` row

### 3) Delete raw lake data

- If using local lake: delete `./.local_lake/raw/channel/<channel_id>/...`
- If using Azure Blob: delete the prefix `raw/channel/<channel_id>/...`

### 4) Delete vector index namespace (if/when enabled)

If a vector store is enabled for your deployment, delete the namespace/prefix for this `channel_id`.

### 5) Verify

- Re-run `/help` in that Telegram chat: bot should respond with “not configured”.
- Ensure no raw blobs remain under the channel prefix.

