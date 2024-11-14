import random

import pytest

from apps.comandas.models import Comanda, ComandaItem
from apps.estoque.models import MovimentacaoEstoque, TiposMovimentacaoEstoqueChoices
from apps.estoque.services import EstoqueProduto

QUANTIDADE_INICIAL = 100
QUANTIDADE_BAIXADA = random.randint(1, QUANTIDADE_INICIAL - 1)
QUANTIDADE_ITENS_ENTREGUE = random.randint(1, 50)


@pytest.fixture
def comanda():
    return Comanda.objects.create(cm_cliente="Teste")


@pytest.fixture
def comanda_itens(comanda, produto):
    items = []
    for _ in range(QUANTIDADE_BAIXADA):
        items.append(
            ComandaItem.objects.create(
                ct_comanda=comanda,
                ct_produto=produto,
            )
        )
    return items


@pytest.fixture
def movimentacao_estoque(produto, comanda_itens):
    return MovimentacaoEstoque.objects.create(
        mv_comanda_item=comanda_itens[0],
        mv_produto=produto,
        mv_tipo=TiposMovimentacaoEstoqueChoices.ENTRADA,
        mv_quantidade=QUANTIDADE_INICIAL,
        mv_quantidade_anterior=0,
        mv_quantidade_atual=QUANTIDADE_INICIAL,
    )


@pytest.mark.django_db
def test_quantidade_total(produto, movimentacao_estoque, comanda, comanda_itens):
    estoque = EstoqueProduto(produto)

    assert estoque.quantidade_total == QUANTIDADE_INICIAL


@pytest.mark.django_db
def test_quantidade_reservada(produto, movimentacao_estoque, comanda, comanda_itens):
    estoque = EstoqueProduto(produto)

    assert estoque.quantidade_reservada == QUANTIDADE_BAIXADA


@pytest.mark.django_db
def test_quantidade_baixada(produto, movimentacao_estoque, comanda, comanda_itens):
    estoque = EstoqueProduto(produto)

    MovimentacaoEstoque.objects.create(
        mv_comanda_item=comanda_itens[0],
        mv_produto=produto,
        mv_tipo=TiposMovimentacaoEstoqueChoices.ENTRADA,
        mv_quantidade=QUANTIDADE_INICIAL,
        mv_quantidade_anterior=movimentacao_estoque.mv_quantidade_atual,
        mv_quantidade_atual=QUANTIDADE_INICIAL,
    )

    assert estoque.quantidade_total == QUANTIDADE_INICIAL
