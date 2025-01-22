from calendar import month_name
from collections import defaultdict

from django.db.models import F, Sum
from django.db.models.functions import ExtractMonth, TruncDate

from .models import Venda, VendaItem


def vendas_por_periodo(data_inicio, data_fim):
    vendas_agregadas = (
        VendaItem.objects.filter(data_criacao__range=[data_inicio, data_fim])
        .annotate(data=TruncDate("data_criacao"), nome_produto=F("vd_produto__pr_nome"))
        .values("data", "nome_produto")
        .annotate(total_faturado=Sum("vd_quantidade"), total_vendido=Sum("vd_valor_total"))
        .order_by("data", "nome_produto")
    )

    totais_diarios = (
        VendaItem.objects.filter(data_criacao__range=[data_inicio, data_fim])
        .annotate(data=TruncDate("data_criacao"))
        .values("data")
        .annotate(valor_total_vendido_dia=Sum("vd_valor_total"), quantidade_total_vendido_dia=Sum("vd_quantidade"))
        .order_by("data")
    )

    totais_por_dia = {
        str(total["data"]): {
            "valor_total_vendido_dia": total["valor_total_vendido_dia"] or 0,
            "quantidade_total_vendido_dia": total["quantidade_total_vendido_dia"] or 0,
        }
        for total in totais_diarios
    }

    vendas_por_dia = defaultdict(
        lambda: {"data": "", "vendas": [], "valor_total_vendido_dia": 0, "quantidade_total_vendido_dia": 0}
    )

    for venda in vendas_agregadas:
        data_str = str(venda["data"])
        vendas_por_dia[data_str]["data"] = data_str
        vendas_por_dia[data_str]["vendas"].append(
            {
                "produto": venda["nome_produto"],
                "total_faturado": venda["total_faturado"] or 0,
                "total_vendido": venda["total_vendido"] or 0,
            }
        )
        vendas_por_dia[data_str].update(
            totais_por_dia.get(data_str, {"valor_total_vendido_dia": 0, "quantidade_total_vendido_dia": 0})
        )

    vendas = [vendas_por_dia[str(data)] for data in sorted(vendas_por_dia.keys())]

    return vendas


def totais_vendas_mensais_ano_atual(ano: int):
    totais_mensais = (
        Venda.objects.filter(data_criacao__year=ano)
        .annotate(mes=ExtractMonth("data_criacao"))
        .values("mes")
        .annotate(valor_total=Sum("vn_valor_total"))
        .order_by("mes")
    )

    resultado = [{"mes": mes, "nome_mes": month_name[mes], "valor_total": 0} for mes in range(1, 13)]

    for total in totais_mensais:
        mes_index = total["mes"] - 1
        resultado[mes_index]["valor_total"] = float(total["valor_total"] or 0)

    return resultado


def top_5_produtos_mais_vendidos(data_inicio, data_fim):
    top_produtos = (
        VendaItem.objects.filter(data_criacao__range=[data_inicio, data_fim])
        .values("vd_produto_id", "vd_produto__pr_nome")
        .annotate(quantidade_total=Sum("vd_quantidade"), valor_total=Sum("vd_valor_total"))
        .order_by("-quantidade_total")
        .values("vd_produto__pr_nome", "quantidade_total", "valor_total")[:5]
    )

    return [
        {
            "produto": item["vd_produto__pr_nome"],
            "quantidade_total": float(item["quantidade_total"] or 0),
            "valor_total": float(item["valor_total"] or 0),
        }
        for item in top_produtos
    ]
