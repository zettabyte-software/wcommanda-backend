import os

from django.core.checks import Error, Tags, register


@register(Tags.compatibility, deploy=True)
def check_required_env_vars(app_configs, **kwargs):
    """Verifica se todas as variáveis de ambiente necessárias estão definidas.

    Levanta ImproperlyConfigured se alguma variável obrigatória estiver faltando.
    """

    envs  = {
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
        "BACKBLAZE_APPLICATION_ID",
        "BACKBLAZE_APPLICATION_KEY",
        "BACKBLAZE_BUCKET_NAME",
        "IFOOD_CLIENT_ID",
        "IFOOD_CLIENT_SECRET",
        "SENTRY_DSN",
        "STRIPE_SECRET_KEY",
        "STRIPE_WEBHOOK_SECRET",
        "TWILLIO_ACCOUNT_SID",
        "TWILLIO_AUTH_TOKEN",
        "TWILLIO_PHONE_NUMBER",
        "CLOUDFLARE_API_TOKEN",
        "WCOMMANDA_SERVER_IP_ADDRESS",
        "WCOMMANDA_ZONE_ID",
    }

    missing = []
    msg = "%s ENV ESTÁ VAZIA"

    for env in envs:
        if env not in os.environ:
            missing.append(
                Error(
                    msg % env,
                    hint="Valor da varíavel de ambiente vazia",
                    id="api.E001",
                )
            )

    return missing


