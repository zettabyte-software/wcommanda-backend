import os

from django.core.checks import Error, Tags, register

from utils.env import ENVS


@register(Tags.compatibility, deploy=True)
def check_required_env_vars(app_configs, **kwargs):
    """Verifica se todas as variáveis de ambiente necessárias estão definidas.

    Levanta ImproperlyConfigured se alguma variável obrigatória estiver faltando.
    """

    missing = []
    msg = "%s ENV ESTÁ VAZIA"

    for env in ENVS:
        if env not in os.environ:
            missing.append(
                Error(
                    msg % env,
                    hint="Valor da varíavel de ambiente vazia",
                    id="api.E001",
                )
            )

    return missing


