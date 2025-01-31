FROM python:3.10-slim AS builder

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /code
RUN useradd --create-home appuser
USER appuser

RUN python -m venv /home/appuser/venv

COPY --chown=appuser:appuser requirements.txt .
RUN /home/appuser/venv/bin/pip install --no-cache-dir -r requirements.txt
RUN /home/appuser/venv/bin/pip install --no-cache-dir gunicorn

FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PATH="/home/appuser/venv/bin:$PATH"

WORKDIR /code
RUN useradd --create-home appuser
USER appuser

COPY --chown=appuser:appuser --from=builder /home/appuser/venv /home/appuser/venv
COPY --chown=appuser:appuser . .