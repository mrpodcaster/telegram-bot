FROM python:3.11-slim AS development

WORKDIR /app

ARG POETRY_HOME=/etc/poetry

COPY poetry.lock pyproject.toml ./

ENV PATH="${PATH}:${POETRY_HOME}/bin"

RUN apt-get update && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get install -y libyaml-dev curl && \
    curl -sSL https://install.python-poetry.org | POETRY_HOME=${POETRY_HOME} python - --version 1.4.0 && \
    apt-get remove -y curl && \
    apt-get autoremove -y && \
    apt-get clean -y && \
    rm -rf /var/lib/apt/lists/* && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-cache && \
    rm -rf ~/.cache ~/.config/pypoetry/auth.toml && \
    poetry install --without dev --sync --no-cache

COPY ./mrpodcaster ./mrpodcaster
COPY manage.py .

RUN python manage.py collectstatic --noinput
