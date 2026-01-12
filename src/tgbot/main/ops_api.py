from __future__ import annotations

import uvicorn

from tgbot.config.settings import get_settings
from tgbot.ops.api.app import create_app


def main() -> None:
    settings = get_settings()
    app = create_app()
    uvicorn.run(app, host=settings.ops_api_bind, port=settings.ops_api_port)


if __name__ == "__main__":
    main()

