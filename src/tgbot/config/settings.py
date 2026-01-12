from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="", case_sensitive=False)

    # Telegram
    telegram_bot_token: str = ""

    # Postgres
    database_url: str = ""

    # Object store (lake)
    tg_object_store: str = "local"  # local|azure
    tg_local_lake_dir: str = "./.local_lake"

    # Queue (event buffer)
    tg_queue: str = "local"  # local|azure
    tg_local_queue_dir: str = "./.local_queue"

    # Ops API
    ops_api_bind: str = "127.0.0.1"
    ops_api_port: int = 8080

    # Safety
    tg_safety_mode: str = "heuristic"

    # Userbot (Telethon) backfill
    telethon_api_id: int = 0
    telethon_api_hash: str = ""
    telethon_session: str = ""  # string session or path supported by Telethon


def get_settings() -> Settings:
    # Import here so python-dotenv is optional at runtime (but available in pyproject).
    try:
        from dotenv import load_dotenv

        load_dotenv()
    except Exception:
        pass
    return Settings()

