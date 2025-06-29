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
from django.contrib.sites.models import Site  # noqa: E402

from django_multitenant.utils import set_current_tenant  # noqa: E402

from apps.filiais.models import Filial  # noqa: E402
from apps.system.assinaturas.models import Assinatura, Plano, StatusChoices, TierChoices  # noqa: E402
from apps.system.core.records import DefaultRecordsManger  # noqa: E402
from apps.users.models import StatusSolicitacaoChoices, Usuario  # noqa: E402

logger = logging.getLogger(__name__)


DEFAULT_SUBDOMAIN = "zettabyte"
DEFAULT_NAME = "Zettabyte"

try:
    site = Site.objects.create(name="wcommanda", domain="api.wcommanda.com.br")

    assinatura = Assinatura.objects.create(
        ss_subdominio=DEFAULT_SUBDOMAIN,
        ss_nome=DEFAULT_NAME,
        ss_cloudflare_id="dev-id",
        ss_status=StatusChoices.ULTRA,
    )

    plano = Plano.objects.create(
        pl_nome="Dev",
        pl_tier=TierChoices.TIER_4,
        pl_numero_usuarios=100,
        pl_integra_ifood=True,
        pl_limite_integracoes_pedidos_ifood=99999,
        pl_valor_mensalidade=0,
        pl_observacao="",
        assinatura=assinatura,
    )

    set_current_tenant(assinatura)

    filial = Filial.objects.create(fl_nome="Dev Wcommanda", assinatura=assinatura)

    usuario = Usuario.objects.create(
        status=StatusSolicitacaoChoices.ACEITO,
        email="davi.s.rafacho@gmail.com",
        password=make_password("dsrafacho!123"),
        first_name="Davi",
        last_name="Silva Rafacho",
        filial=filial,
        assinatura=assinatura,
    )

    DefaultRecordsManger().apply_updates()
    logger.info("Assinatura de desenvolvimento criada com sucesso!")
except Exception as e:
    logger.error("Ocorreu um erro inesperado ao criar a assinatura de desenvolvimento: \n%s", e)
