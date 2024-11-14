from apps.comandas.models import Comanda
from apps.financeiro.models import Pagamento
from apps.users.models import Usuario

from .models import Venda, VendaItem


def gerar_venda_por_comanda(comanda: Comanda, user: Usuario):
    venda = Venda(
        vn_comanda=comanda,
        vn_cliente=comanda.cm_cliente,
        vn_valor_total=comanda.cm_valor_total,
        owner=user,
    )

    venda.save()

    todos_itens_comanda = comanda.itens.all()
    itens_comanda_por_produto = (
        comanda.itens.all()
        .order_by("ct_produto__id")
        .distinct("ct_produto__id")
    )
    for item in itens_comanda_por_produto:
        quantidade = todos_itens_comanda.filter(ct_produto=item.ct_produto).count()
        VendaItem.objects.create(
            vd_venda=venda,
            vd_quantidade=quantidade,
            vd_produto=item.ct_produto,
            vd_preco_unitario_produto=item.ct_preco_unitario_produto,
            vd_valor_total=item.ct_preco_unitario_produto * quantidade,
            owner=user,
        )

    Pagamento.objects.create(
        pg_venda=venda,
        pg_parcela=1,
        pg_valor=comanda.cm_valor_total,
        pg_forma_pagamento=comanda.cm_forma_pagamento,
        owner=user,
    )

    return venda
