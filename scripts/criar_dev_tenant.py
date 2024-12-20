import logging
import os
import sys

import django

import dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "api.settings")

dotenv.load_dotenv()

django.setup()

from django.contrib.auth.hashers import make_password  # noqa: E402

from apps.system.tenants.models import Ambiente  # noqa: E402
from apps.users.models import Usuario  # noqa: E402

logger = logging.getLogger(__name__)


DEFAULT_SUBDOMAIN = "zettabyte"
DEFAULT_NAME = "Zettabyte"

try:
    ambiente = Ambiente.objects.create(mb_subdominio=DEFAULT_SUBDOMAIN, mb_nome=DEFAULT_NAME)
    usuario = Usuario.objects.create(
        email="",
        password=make_password(""),
        first_name="",
        last_name="",
        ambiente=ambiente,
    )
    logging.info("Tenant de desenvolvimento criado com sucesso!")
except Exception as e:
    logging.error("Ocorreu um erro inesperado ao criar o tenant de desenvolvimento: \n%s", e)
