from utils.env import get_env_var

from .models import Configuracao
from .types import TCodigoConfiguracao


def get_configuracao(codigo: TCodigoConfiguracao):
    risky = get_env_var("DJANGO_EXECUTION_MODE") == "risky"
    if risky:
        param = Configuracao.objects.get(cf_codigo=codigo)
    else:
        param = Configuracao.objects.filter(cf_codigo=codigo).last()

    return Configuracao.normalize_value(codigo, param.cf_valor)
