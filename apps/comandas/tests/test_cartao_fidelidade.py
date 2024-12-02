import random

import pytest

from apps.clientes.models import Cliente
from apps.comandas.models import Comanda, ComandaItem

QUANTIDADE_ITENS = random.randint(1, 99)


@pytest.fixture
def cliente_fidelidade():
    return Cliente.objects.create(cl_nome="Roberto", cl_sobrenome="Rigamonte")


@pytest.fixture
def comanda_com_cliente_fidelidade(usuario, produto, cliente_fidelidade):
    comanda = Comanda.objects.create(cm_cliente="Roberto", cm_garcom=usuario, cm_cliente_fidelidade=cliente_fidelidade)
    itens = []
    for _ in range(QUANTIDADE_ITENS):
        item = ComandaItem()
        item.ct_comanda = comanda
        item.ct_produto = produto
        item.ct_preco_unitario_produto = produto.pr_preco
        itens.append(item)

    ComandaItem.objects.bulk_create(itens)
    return comanda


@pytest.fixture
def condicao_premio():
    pass


@pytest.fixture
def premio():
    pass


@pytest.fixture
def cartao_fidelidade(condicao_premio, premio):
    pass


@pytest.mark.skip("Não implementado")
def test_carimbo(comanda_com_cliente_fidelidade, configuracoes):
    pass
