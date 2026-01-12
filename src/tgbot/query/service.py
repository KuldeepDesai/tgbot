from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone

from tgbot.query.recommendations import Recommendation, build_recommendations
from tgbot.storage.repos.messages_repo import MessagesRepo


@dataclass(frozen=True)
class QueryResult:
    cutoff_ts: datetime
    recommendations: list[Recommendation]


def answer_query(
    *,
    channel_id: str,
    query_text: str,
    messages_repo: MessagesRepo,
    max_distinct: int = 12,
) -> QueryResult:
    # Simple keyword search and dedupe-by-provider.
    terms = [t.strip().lower() for t in (query_text or "").split() if t.strip()]
    candidates = messages_repo.search_text(channel_id=channel_id, query_terms=terms, limit=500)
    cutoff = max((m.ts for m in candidates), default=datetime.now(timezone.utc))
    recs = build_recommendations(candidates, max_distinct=max_distinct)
    return QueryResult(cutoff_ts=cutoff, recommendations=recs)

