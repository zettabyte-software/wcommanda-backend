FROM python:3.13-alpine AS builder

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apk add --no-cache \
    build-base \
    postgresql-dev

WORKDIR /code
RUN adduser -D appuser
USER appuser

RUN python -m venv /home/appuser/venv

COPY --chown=appuser:appuser requirements.txt .
RUN /home/appuser/venv/bin/pip install --no-cache-dir -r requirements.txt
RUN /home/appuser/venv/bin/pip install --no-cache-dir gunicorn

FROM python:3.13-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/home/appuser/venv/bin:$PATH"

WORKDIR /code

RUN adduser -D appuser

RUN mkdir -p /code/logs && chmod -R 777 /code/logs
RUN mkdir -p /code/logs/gunicorn && chmod -R 777 /code/logs/gunicorn

USER appuser

COPY --chown=appuser:appuser --from=builder /home/appuser/venv /home/appuser/venv
COPY --chown=appuser:appuser . .

CMD [  ]