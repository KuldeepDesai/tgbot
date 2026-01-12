from datetime import datetime, timezone

from tgbot.ingestion.schema.event_envelope import EventEnvelope


def test_event_envelope_has_required_fields():
    env = EventEnvelope(
        source="bot_api",
        telegram_chat_id="123",
        channel_id="ch_1",
        event_type="message_new",
        message_id=10,
        payload={"update_id": 1},
    )
    assert env.event_id
    assert isinstance(env.received_at, datetime)
    assert env.received_at.tzinfo is not None
    assert env.received_at.tzinfo == timezone.utc
    assert env.schema_version == 1

