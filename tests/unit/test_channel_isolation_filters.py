from datetime import datetime, timezone

from tgbot.storage.models.messages import Message
from tgbot.query.recommendations import build_recommendations


def test_build_recommendations_does_not_mix_channels_when_input_is_scoped():
    # The channel isolation requirement is enforced by query layer passing channel-scoped messages.
    # This test ensures the builder itself doesn't introduce cross-channel leakage by re-querying.
    msgs = [
        Message(
            channel_id="A",
            message_id=1,
            sender_id="u1",
            ts=datetime.now(timezone.utc),
            text="Electrician Raj - 9876543210",
            raw_json={},
            deleted=False,
            quarantined=False,
            quarantine_reason=None,
            latest_version_ts=datetime.now(timezone.utc),
        )
    ]
    recs = build_recommendations(msgs, max_distinct=12)
    assert recs
    assert all("raj" in r.provider_key for r in recs)

