from __future__ import annotations

from fastapi import FastAPI

from tgbot.ops.api.routes.broadcast import router as broadcast_router
from tgbot.ops.api.routes.health import router as health_router


def create_app() -> FastAPI:
    app = FastAPI(title="tgbot ops", version="0.1.0")
    app.include_router(health_router, prefix="/ops/v1")
    app.include_router(broadcast_router, prefix="/ops/v1")
    return app

