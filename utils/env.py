import ast
import os
from typing import Literal

ENVS  = {
    # api
    "DJANGO_SECRET_KEY",
    "DJANGO_DEBUG",
    "DJANGO_MODE",
    "DJANGO_EXECUTION_MODE",
    "DJANGO_LOG_LEVEL",

    "DATABASE_NAME",
    "DATABASE_USER",
    "DATABASE_PASSWORD",
    "DATABASE_HOST",
    "DATABASE_PORT",

    "REDIS_HOST",
    "REDIS_PORT",

    "EMAIL_PASSWORD",

    "RABBITMQ_CONNECTION_STRING",

    # back blaze
    "BACKBLAZE_APPLICATION_ID",
    "BACKBLAZE_APPLICATION_KEY",
    "BACKBLAZE_BUCKET_NAME",

    # sentry
    "SENTRY_DSN",

    # stripe
    "STRIPE_SECRET_KEY",
    "STRIPE_WEBHOOK_SECRET",

    # twilio
    "TWILLIO_ACCOUNT_SID",
    "TWILLIO_AUTH_TOKEN",
    "TWILLIO_PHONE_NUMBER",

    # cloudflare
    "CLOUDFLARE_API_TOKEN",

    # wcommanda
    "WCOMMANDA_SERVER_IP_ADDRESS",
    "WCOMMANDA_ZONE_ID",
}

EnviromentVar = Literal[
    # api
    "DJANGO_SECRET_KEY",
    "DJANGO_DEBUG",
    "DJANGO_MODE",
    "DJANGO_EXECUTION_MODE",
    "DJANGO_LOG_LEVEL",

    "DATABASE_NAME",
    "DATABASE_USER",
    "DATABASE_PASSWORD",
    "DATABASE_HOST",
    "DATABASE_PORT",

    "REDIS_HOST",
    "REDIS_PORT",

    "EMAIL_PASSWORD",

    "RABBITMQ_CONNECTION_STRING",

    # back blaze
    "BACKBLAZE_APPLICATION_ID",
    "BACKBLAZE_APPLICATION_KEY",
    "BACKBLAZE_BUCKET_NAME",

    # sentry
    "SENTRY_DSN",

    # stripe
    "STRIPE_SECRET_KEY",
    "STRIPE_WEBHOOK_SECRET",

    # twilio
    "TWILLIO_ACCOUNT_SID",
    "TWILLIO_AUTH_TOKEN",
    "TWILLIO_PHONE_NUMBER",

    # cloudflare
    "CLOUDFLARE_API_TOKEN",

    # wcommanda
    "WCOMMANDA_SERVER_IP_ADDRESS",
    "WCOMMANDA_ZONE_ID",
]


def get_env_var(key: EnviromentVar):
    return os.environ.get(key)


def get_bool_from_env(key: EnviromentVar, default_value):
    if key in os.environ:
        value = os.environ[key]
        try:
            return ast.literal_eval(value)
        except ValueError as exc:
            raise ValueError(f"'{value}' não é um valor válido para '{key}'") from exc
    return default_value
