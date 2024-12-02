import random

import pytest

from apps.comandas.models import Comanda, ComandaItem
from apps.comandas.services import gerar_comissao_garcom
from apps.system.conf.services import get_configuracao

QUANTIDADE_PRODUTOS = random.randint(1, 99)


@pytest.fixture
def comanda_com_comissao(usuario, produto):
    comanda = Comanda.objects.create(cm_cliente="Teste", cm_garcom=usuario)
    itens = []
    for _ in range(QUANTIDADE_PRODUTOS):
        item = ComandaItem()
        item.ct_comanda = comanda
        item.ct_produto = produto
        item.ct_preco_unitario_produto = produto.pr_preco
        itens.append(item)

    ComandaItem.objects.bulk_create(itens)
    return comanda


@pytest.mark.django_db
def test_comissao(comanda_com_comissao, configuracoes):
    percentual_comissao = get_configuracao("WCM_PERCENTUAL_COMISSAO_GARCON")
    comissao = gerar_comissao_garcom(comanda_com_comissao)
    assert comanda_com_comissao.cm_valor_comissao == comissao.cg_valor
    assert comissao.cg_percentual == percentual_comissao
