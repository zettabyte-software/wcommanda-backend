from django.db.models import Sum

from apps.produtos.models import Produto
from utils.date import gerar_dias_entre_2_datas

from .models import VendaItem


def vendas_por_periodo(data_inicio, data_fim):
    produtos = Produto.objects.all().only("id", "pr_nome")
    vendas = []
    datas = gerar_dias_entre_2_datas(data_inicio, data_fim)
    for data in datas:
        informacoes_vendas = []
        valor_total_vendido_dia = VendaItem.objects.filter(data_criacao=data).aggregate(total=Sum("vd_valor_total"))["total"]
        quantidade_total_vendido_dia = VendaItem.objects.filter(data_criacao=data).aggregate(total=Sum("vd_quantidade"))["total"]

        for produto in produtos:
            itens_vendidos = VendaItem.objects.filter(
                vd_produto=produto,
                data_criacao=data,
            )

            quantidade_total = itens_vendidos.aggregate(total=Sum("vd_quantidade"))["total"]
            valor_total = itens_vendidos.aggregate(total=Sum("vd_valor_total"))["total"]

            informacoes_vendas.append(
                {
                    "produto": produto.pr_nome,
                    "total_faturado": quantidade_total or 0,
                    "total_vendido": valor_total or 0,
                }
            )

        vendas.append(
            {
                "data": data.strftime("%Y-%m-%d"),
                "vendas": informacoes_vendas,
                "valor_total_vendido_dia": valor_total_vendido_dia or 0,
                "quantidade_total_vendido_dia": quantidade_total_vendido_dia or 0,
            }
        )

    return vendas
