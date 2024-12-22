import json
import os

from rest_framework.test import APIClient

import dotenv
import pytest
from auditlog.registry import auditlog
from django_multitenant.utils import set_current_tenant
from threadlocals.threadlocals import set_current_user

from apps.mesas.models import Mesa
from apps.produtos.models import Produto
from apps.system.conf.models import Configuracao
from apps.system.tenants.models import Ambiente
from apps.users.models import Usuario

dotenv.load_dotenv()

os.environ["DJANGO_MODE"] = "testing"


@pytest.fixture(autouse=True)
def _use_test_database(settings):
    settings.DATABASES["default"]["NAME"] = "test_wcommanda"


@pytest.fixture(autouse=True)
def disable_auditlog_fixture():
    for model in auditlog.get_models():
        auditlog.unregister(model)


@pytest.fixture(autouse=True)
def _use_dummy_cache_backend(settings):
    settings.CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.dummy.DummyCache",
        }
    }


@pytest.fixture(autouse=True)
def ambiente():
    ambiente = Ambiente.objects.create(mb_nome="Teste", mb_subdominio="teste")
    set_current_tenant(ambiente)
    return ambiente


@pytest.fixture(autouse=True)
def usuario():
    usuario = Usuario.objects.create(
        first_name="Davi",
        last_name="Silva Rafacho",
        email="exemplo@gmail.com",
        password="exemplo@gmail.com",
    )
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
    )


@pytest.fixture
def api_client(usuario):
    client = APIClient()
    client.force_authenticate(user=usuario)
    return client


@pytest.fixture
def mesa():
    return Mesa.objects.create(ms_codigo=1, ms_quantidade_lugares=4)
