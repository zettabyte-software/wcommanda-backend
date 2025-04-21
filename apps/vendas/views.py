import calendar

from django.db.models import Count, F, Sum
from django.utils import timezone

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .dashboards import vendas_por_periodo
from .models import Venda, VendaItem
from .serializers import DashboardQueryParamSerializer


class DashboardVendasViewSet(GenericViewSet):
    @action(methods=["get"], detail=False)
    def por_dias(self, request):
        serializer = DashboardQueryParamSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        dados = serializer.validated_data
        vendas = vendas_por_periodo(dados["data_inicio"], dados["data_fim"])
        return Response({"vendas": vendas})

    @action(methods=["get"], detail=False)
    def produtos_mais_vendidos(self, request):
        serializer = DashboardQueryParamSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        data_inicio = serializer.data["data_inicio"]
        data_fim = serializer.data["data_fim"]

        vendas = Venda.objects.filter(data_criacao__range=(data_inicio, data_fim))

        itens_vendas = VendaItem.objects.filter(vd_venda__in=(vendas))
        vendas_produtos = (
            itens_vendas.values("vd_produto__pr_nome")
            .annotate(
                total_items_produto=Count("vd_produto__pr_nome"),
                total_vendido=Sum("vd_quantidade"),
            )
            .order_by(
                "-total_vendido",
            )
        )

        dados_dashboard = []
        ultimos_5_items = vendas_produtos[:5]
        for item in ultimos_5_items:
            produto = item["vd_produto__pr_nome"]
            dados = {"produto": produto, "quantidade": item["total_vendido"]}
            dados_dashboard.append(dados)

        return Response({"dashboard": dados_dashboard})

    @action(methods=["get"], detail=False)
    def vendas_anual(self, request):
        hoje = timezone.now().date()
        primeiro_dia_mes = hoje.replace(day=1)
        _, numero_ultimo_dia = calendar.monthrange(hoje.year, hoje.month)
        ultimo_dia_mes = hoje.replace(day=numero_ultimo_dia)

        meses_ano = {
            "1": "Janeiro",
            "2": "Fevereiro",
            "3": "Março",
            "4": "Abril",
            "5": "Maio",
            "6": "Junho",
            "7": "Julho",
            "8": "Agosto",
            "9": "Setembro",
            "10": "Outubro",
            "11": "Novembro",
            "12": "Dezembro",
        }

        itens_vendas = (
            VendaItem.objects.filter(
                data_criacao__range=(primeiro_dia_mes, ultimo_dia_mes)
            )
            .values("data_criacao")
            .annotate(total=Sum(F("vd_quantidade") * F("vd_preco_unitario_produto")))
            .order_by("data_criacao")
        )

        dados_dashboard = []
        for mes_d, mes_s in meses_ano.items():
            dados = {}
            for item in itens_vendas:
                data = item["data_criacao"]
                total = item["total"]
                if data.month == int(mes_d):
                    dados["mes"] = mes_s
                    dados["total"] = total
                    break
            else:
                dados["mes"] = mes_s
                dados["total"] = 0.0

            dados_dashboard.append(dados)

        return Response({"dashboard": dados_dashboard})

