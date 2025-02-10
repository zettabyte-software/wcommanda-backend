import datetime

from django.db.models.aggregates import Sum

from apps.vendas.models import Venda


class RankingClientes:
    def __init__(self, data_incio: datetime.date, data_fim: datetime.date):
        self.vendas = Venda.objects.filter(data_criacao__range=(data_incio, data_fim))

    def calcular_top_5_clientes(self):
        ranking = (
            self.vendas.filter(vn_cliente_fidelidade__isnull=False)
            .values("vn_cliente")
            .annotate(total_gasto=Sum("vn_valor_total"))
            .order_by("-total_gasto")[:5]
        )

        return ranking
