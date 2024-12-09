FROM python:3.12.6-slim AS base
LABEL authors="lazzarusxd"

ENV PYTHONUNBUFFERED=1
ENV PATH="/root/.local/bin:$PATH"
ENV PYTHONPATH='/'

COPY poetry.lock pyproject.toml ./

WORKDIR /app

RUN pip install --no-cache-dir poetry \
    && poetry install --no-root --only main

COPY ./app /app