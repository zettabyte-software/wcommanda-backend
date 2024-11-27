from calendar import monthrange
from datetime import date, datetime

from django.db.models import Count, F, Sum

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from apps.comandas.models import ComandaItem, StatusComandaChoices
from apps.system.base.views import BaseModelViewSet

from .serializers import (
    CategoriaProduto,
    CategoriaProdutoSerializer,
    Produto,
    ProdutoAlteracaoSerializer,
    ProdutoVisualizacaoSerializer,
)
from .services import gerar_codigo_cardapio


class CategoriaProdutoViewSet(BaseModelViewSet):
    queryset = CategoriaProduto.objects.all()
    serializer_class = CategoriaProdutoSerializer


class ProdutoViewSet(BaseModelViewSet):
    queryset = Produto.objects.all()
    serializer_classes = {
        "list": ProdutoVisualizacaoSerializer,
        "retrieve": ProdutoVisualizacaoSerializer,
        "create": ProdutoAlteracaoSerializer,
        "update": ProdutoAlteracaoSerializer,
        "partial_update": ProdutoAlteracaoSerializer,
        "bulk_create": ProdutoAlteracaoSerializer,
        "clonar": ProdutoAlteracaoSerializer,
    }
    filterset_fields = {
        "id": ["exact"],
        "pr_nome": ["icontains"],
        "pr_codigo_cardapio": ["exact", "icontains"],
        "pr_preco": ["icontains"],
        "pr_tempo_preparo": ["icontains"],
        "pr_controla_estoque": ["exact"],
        "pr_categoria__cg_nome": ["icontains"],
    }
    search_fields = ["pr_nome", "pr_codigo_cardapio"]

    @action(methods=["get"], detail=False)
    def sugestao_codigo_cardapio(self, request):
        codigo = gerar_codigo_cardapio()
        return Response({"pr_codigo_cardapio": codigo})

    def alterar_campos_unicos(self, instance):
        instance.pr_codigo_cardapio = gerar_codigo_cardapio()


class RelatorioViewSet(ViewSet):
    hoje = date.today()
    primeiro_dia_mes = hoje.replace(day=1)
    _, numero_ultimo_dia = monthrange(hoje.year, hoje.month)
    ultimo_dia_mes = hoje.replace(day=numero_ultimo_dia)

    @action(methods=["get"], detail=False)
    def fluxo_caixa(self, request):
        hoje = datetime.now().strftime("%Y-%m-%d")

        produtos = (
            ComandaItem.objects.filter(
                ct_comanda__data_criacao=hoje,
                ct_comanda__status=StatusComandaChoices.FINALIZADA,
            )
            .order_by("ct_produto__id")
            .distinct("ct_produto")
            .values("ct_produto__id", "ct_produto__nome")
        )

        fluxo_produtos = []
        for produto in produtos:
            itens = ComandaItem.objects.filter(produto__id=produto["produto__id"])
            valores_venda = itens.aggregate(
                quantidade_total=Sum("quantidade"),
                valor_total=Sum(F("quantidade") * F("preco_unitario_produto")),
            )

            fluxo_produtos.append(
                {
                    "produto": produto["produto__nome"],
                    "quantidade_total_vendida": round(valores_venda["quantidade_total"], 2),
                    "valor_total_faturado": round(valores_venda["valor_total"], 2),
                }
            )

        return Response({"fluxo_produtos": fluxo_produtos})

    @action(methods=["get"], detail=False)
    def vendas_por_produto(self, request):
        produtos = Produto.objects.all()
        resultados = []
        for produto in produtos:
            itens = ComandaItem.objects.filter(
                comanda__data_criacao__range=(
                    self.primeiro_dia_mes,
                    self.ultimo_dia_mes,
                ),
                produto=produto,
                comanda__status=StatusComandaChoices.FINALIZADA,
            )

            if itens.count() == 0:
                resultados.append(
                    {
                        "produto": produto.nome,
                        "quantidade_total_vendida": 0,
                        "valor_total_faturado": 0,
                    }
                )

                continue
            valores = itens.aggregate(
                quantidade_total_vendida=Sum("quantidade") or 0,
                valor_total_faturado=Sum(F("quantidade") * F("preco_unitario_produto")) or 0,
            )

            resultados.append(
                {
                    "produto": produto.nome,
                    "quantidade_total_vendida": round(valores["quantidade_total_vendida"], 2),
                    "valor_total_faturado": round(valores["valor_total_faturado"], 2),
                }
            )

        return Response({"vendas_produto": resultados})


class DashboardViewSet(ViewSet):
    hoje = date.today()
    primeiro_dia_mes = hoje.replace(day=1)
    _, numero_ultimo_dia = monthrange(hoje.year, hoje.month)
    ultimo_dia_mes = hoje.replace(day=numero_ultimo_dia)

    @action(methods=["get"], detail=False)
    def produtos_mais_vendidos_mes(self, request):
        items = (
            ComandaItem.objects.filter(
                comanda__data_criacao__range=(
                    self.primeiro_dia_mes,
                    self.ultimo_dia_mes,
                ),
                comanda__status=StatusComandaChoices.FINALIZADA,
            )
            .values("produto__nome")
            .annotate(
                total_items_produto=Count("produto__nome"),
                total_vendido=Sum("quantidade"),
            )
            .order_by(
                "-total_vendido",
            )
        )

        itens_map = {}
        ultimos_5_items = items[:5]
        for item in ultimos_5_items:
            produto = item["produto__nome"]
            itens_map[produto] = item["total_vendido"]

        return Response(itens_map)

    @action(methods=["get"], detail=False)
    def vendas_anual(self, request):
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

        itens = (
            ComandaItem.objects.filter(
                comanda__data_criacao__range=(
                    self.primeiro_dia_mes,
                    self.ultimo_dia_mes,
                ),
                comanda__status=StatusComandaChoices.FINALIZADA,
            )
            .values("data_criacao")
            .annotate(total=Sum(F("quantidade") * F("preco_unitario_produto")))
            .order_by("data_criacao")
        )

        resultados = {}
        for mes_d, mes_s in meses_ano.items():
            for item in itens:
                data = item["data_criacao"]
                total = item["total"]
                if data.month == int(mes_d):
                    resultados[mes_s] = total
                    break
            else:
                resultados[mes_s] = 0

        return Response(resultados)

    @action(methods=["get"], detail=False)
    def kpis(self, request):
        base_queryset = ComandaItem.objects.filter(
            comanda__data_criacao__range=(
                self.primeiro_dia_mes,
                self.ultimo_dia_mes,
            ),
            comanda__status=StatusComandaChoices.FINALIZADA,
        )

        analises = base_queryset.aggregate(
            total_faturado=Sum(F("quantidade") * F("preco_unitario_produto")),
            total_vendida=Sum("quantidade"),
        )

        quantidade_produtos_vendida = base_queryset.order_by("produto__id").distinct("produto__id").count()

        quantidade_total_produtos = Produto.objects.all().count()

        total_faturado = analises["total_faturado"] or 0
        total_vendida = analises["total_vendida"] or 0
        total_comandas = base_queryset.order_by("comanda__id").distinct("comanda__id").count()
        analise_produtos = quantidade_total_produtos - quantidade_produtos_vendida

        return Response(
            {
                "total_faturado": total_faturado,
                "total_vendida": total_vendida,
                "total_comandas": total_comandas,
                "analise_produtos": analise_produtos,
            }
        )
