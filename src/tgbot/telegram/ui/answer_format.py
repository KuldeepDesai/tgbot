from __future__ import annotations

from datetime import datetime

from tgbot.query.recommendations import Recommendation
from tgbot.telegram.markdown_v2 import escape_markdown_v2
from tgbot.time.formatters import format_date_ist, format_ist_minute


def _format_citations(rec: Recommendation) -> str:
    parts: list[str] = []
    for c in rec.citations[:3]:
        date = format_date_ist(c.message_ts)
        # Prefer link when possible; fallback to a stable text citation.
        if c.url:
            parts.append(f"[{escape_markdown_v2('msg ' + str(c.message_id))}]({escape_markdown_v2(c.url)}) ({date})")
        else:
            parts.append(f"{escape_markdown_v2('msg ' + str(c.message_id))} ({date})")
    return "; ".join(parts) if parts else "n/a"


def format_answer_markdown_v2(
    *,
    query_text: str,
    cutoff_ts_utc: datetime,
    recommendations: list[Recommendation],
    show_disagreement_note: bool,
) -> str:
    lines: list[str] = []
    cutoff = format_ist_minute(cutoff_ts_utc)
    lines.append(f"*{escape_markdown_v2('Top recommendations')}*")
    lines.append(f"_Based on messages up to {escape_markdown_v2(cutoff)} (IST)_")
    lines.append("")

    if show_disagreement_note:
        lines.append(
            escape_markdown_v2(
                "Note: Some messages show conflicting opinions. I’ve included citations and dates so you can verify both sides."
            )
        )
        lines.append("")

    if not recommendations:
        lines.append(escape_markdown_v2("I couldn’t find strong matches in this channel yet."))
        return "\n".join(lines)

    for idx, rec in enumerate(recommendations, start=1):
        title = escape_markdown_v2(rec.title or rec.provider_key)
        lines.append(f"*{idx}.* {title}")
        if rec.contacts:
            lines.append(f"  - {escape_markdown_v2('Contact')}: {escape_markdown_v2(', '.join(rec.contacts))}")
        lines.append(f"  - {escape_markdown_v2('Citations')}: {_format_citations(rec)}")

    return "\n".join(lines)

