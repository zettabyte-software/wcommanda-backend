from django.utils import timezone

import pytest

from apps.comandas.models import Comanda
from apps.comandas.services import atualizar_codigo_comanda


@pytest.mark.django_db
def test_atualizador_codigo_comanda():
    comanda = Comanda.objects.create(cm_cliente="Teste")
    atualizar_codigo_comanda(comanda)

    comanda2 = Comanda.objects.create(cm_cliente="Teste 1")
    atualizar_codigo_comanda(comanda2)

    comanda3 = Comanda.objects.create(cm_cliente="Teste 2")
    atualizar_codigo_comanda(comanda3)

    assert comanda.cm_codigo == 1
    assert comanda2.cm_codigo == 2

    assert comanda3.cm_codigo == 3


@pytest.mark.django_db
def test_reinicio_codigo_comanda(configuracoes: dict):
    reinicio = configuracoes["WCM_REINICIO_CODIGO_COMANDA"]
    reinicio.cf_valor = False
    reinicio.save()

    comanda = Comanda.objects.create(cm_cliente="Teste")
    atualizar_codigo_comanda(comanda)

    comanda2 = Comanda.objects.create(cm_cliente="Teste 1")
    atualizar_codigo_comanda(comanda2)

    comanda3 = Comanda.objects.create(cm_cliente="Teste 2")
    atualizar_codigo_comanda(comanda3)

    amanha = timezone.now() + timezone.timedelta(days=1)
    comanda4 = Comanda.objects.create(cm_cliente="Teste 4", data_criacao=amanha)
    atualizar_codigo_comanda(comanda4)

    assert comanda4.cm_codigo == 4

    reinicio.cf_valor = True
    reinicio.save()
