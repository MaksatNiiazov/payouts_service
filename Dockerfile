FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app

# system deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    netcat-openbsd \
    curl \
    && rm -rf /var/lib/apt/lists/*

# install poetry
RUN pip install --no-cache-dir poetry

# build arg: install dev deps or not
ARG INSTALL_DEV=false

COPY pyproject.toml poetry.lock* /app/

RUN if [ "$INSTALL_DEV" = "true" ]; then \
        poetry install --no-interaction --no-ansi --all-extras ; \
    else \
        poetry install --no-interaction --no-ansi ; \
    fi

COPY . /app/

ENTRYPOINT ["/app/entrypoint.sh"]
