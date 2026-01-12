FROM python:3.11-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# System deps (keep minimal; psycopg[binary] doesn't need build tooling)
RUN apt-get update \
  && apt-get install -y --no-install-recommends ca-certificates \
  && rm -rf /var/lib/apt/lists/*

# Install app + dependencies
COPY pyproject.toml README.md /app/
COPY src /app/src
COPY migrations /app/migrations
COPY alembic.ini /app/alembic.ini

RUN python -m pip install --upgrade pip \
  && python -m pip install .

# Default env suitable for containers; override via compose/env
ENV OPS_API_BIND=0.0.0.0

CMD ["python", "-m", "tgbot.main.receiver"]
