from __future__ import annotations

import asyncio

from tgbot.telegram.updates.receiver_polling import run_polling


def main() -> None:
    asyncio.run(run_polling())


if __name__ == "__main__":
    main()

