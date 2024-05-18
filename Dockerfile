FROM python:3.11-slim as staging

ARG POETRY_HOME=/etc/poetry
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1

WORKDIR /

RUN apt-get update && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get install -y libyaml-dev curl tini && \
    curl -sSL https://install.python-poetry.org | POETRY_HOME=${POETRY_HOME} python - --version 1.7.1 && \
    apt-get remove -y curl && \
    apt-get autoremove -y && \
    apt-get clean -y && \
    rm -rf /var/lib/apt/lists/*

ENV PATH="${PATH}:${POETRY_HOME}/bin"

COPY ./pyproject.toml ./poetry.lock ./

RUN poetry export -o /requirements.txt

FROM python:3.11-slim as prod

WORKDIR /

COPY --from=staging /requirements.txt /requirements.txt

RUN python -m venv venv &&\
    pip install -r requirements.txt

COPY ./manage.py /
COPY ./mrpodcaster /mrpodcaster
RUN python ./manage.py collectstatic --noinput
