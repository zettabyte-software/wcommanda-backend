import json
import os

from django.core.cache import cache

from rest_framework.test import APIClient

import dotenv
import pytest
from auditlog.registry import auditlog
from django_multitenant.utils import set_current_tenant
from threadlocals.threadlocals import set_current_user

from apps.mesas.models import Mesa
from apps.produtos.models import Produto
from apps.system.assinaturas.models import Assinatura, Plano, TierChoices
from apps.system.conf.models import Configuracao
from apps.users.models import Usuario

dotenv.load_dotenv()

os.environ["DJANGO_MODE"] = "testing"


@pytest.fixture(autouse=True)
def use_test_database(settings):
    settings.DATABASES["default"]["NAME"] = "test_wcommanda"


@pytest.fixture(autouse=True)
def disable_auditlog_fixture():
    for model in auditlog.get_models():
        auditlog.unregister(model)


@pytest.fixture(autouse=True)
def use_dummy_cache_backend(settings):
    cache.clear()
    settings.CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.dummy.DummyCache",
        }
    }


@pytest.fixture(autouse=True)
def assinatura():
    plano = Plano.objects.create(
        pl_nome="Dev",
        pl_tier=TierChoices.TIER_4,
        pl_numero_usuarios=100,
        pl_integra_ifood=True,
        pl_limite_integracoes_pedidos_ifood=99999,
        pl_valor_mensalidade=0,
        pl_observacao="",
    )

    assinatura = Assinatura.objects.create(
        ss_nome="Teste",
        ss_subdominio="teste",
        ss_cloudflare_id="test-id",
        ss_plano=plano,
    )

    set_current_tenant(assinatura)

    return assinatura


@pytest.fixture(autouse=True)
def usuario():
    usuario = Usuario.objects.create(
        first_name="Davi",
        last_name="Silva Rafacho",
        email="exemplo@gmail.com",
        password="",
    )
    usuario.set_unusable_password()
    set_current_user(usuario)
    return usuario


@pytest.fixture(autouse=True)
def configuracoes():
    json_configuracoes = json.load(open("data/records/default/configuracoes.json"))
    for dados in json_configuracoes:
        Configuracao.objects.create(**dados["data"])
    return {c.cf_codigo: c for c in Configuracao.objects.all()}


@pytest.fixture
def produto():
    return Produto.objects.create(
        pr_codigo_cardapio="1",
        pr_nome="KitKat® Thunder & S'mores",
        pr_descricao="A novidade brookie, que é um brownie de chocolate com noz pecan.",
        pr_preco=85,
        pr_tempo_preparo=15,
        pr_path_imagem="undefined",
        pr_id_back_blaze="undefined",
    )


@pytest.fixture
def api_client(usuario):
    client = APIClient()
    client.force_authenticate(user=usuario)
    return client


@pytest.fixture
def mesa():
    return Mesa.objects.create(ms_codigo=1, ms_quantidade_lugares=4)
