from rest_framework.decorators import action
from rest_framework.response import Response

from threadlocals.threadlocals import get_request_variable

from apps.ifood.integradores.categorias import IntegradorCategoriasIfood
from apps.ifood.integradores.produtos import IntegradorProdutoIfood
from apps.system.base.views import BaseModelViewSet

from .serializers import (
    CategoriaProduto,
    CategoriaProdutoSerializer,
    # ComplementoProduto,
    # ComplementoProdutoAlteracaoSerializer,
    # ComplementoProdutoVisualizacaoSerializer,
    CustomizacaoProduto,
    CustomizacaoProdutoAlteracaoSerializer,
    CustomizacaoProdutoItem,
    CustomizacaoProdutoItemAlteracaoSerializer,
    CustomizacaoProdutoItemVisualizacaoSerializer,
    CustomizacaoProdutoVisualizacaoSerializer,
    # GrupoComplementoProduto,
    # GrupoComplementoProdutoAlteracaoSerializer,
    # GrupoComplementoProdutoVisualizacaoSerializer,
    Produto,
    ProdutoAlteracaoSerializer,
    ProdutoVisualizacaoSerializer,
)
from .services import gerar_codigo_cardapio


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

    """ TODO pensar um jeito melhor de fazer a sincronização do ifood
    def perform_create(self, serializer, **overwrite):
        instance = super().perform_create(serializer, **overwrite)

        filial = get_request_variable("filial")

        if filial is None:
            return

        merchant_id = filial.fl_merchat_id_ifood

        integrador = IntegradorProdutoIfood(merchant_id)
        integrador.sincronizar_alteracoes(instance)

    def perform_update(self, serializer, **overwrite):
        instance = super().perform_update(serializer, **overwrite)

        filial = get_request_variable("filial")

        if filial is None:
            return

        merchant_id = filial.fl_merchat_id_ifood

        integrador = IntegradorProdutoIfood(merchant_id)
        integrador.sincronizar_alteracoes(instance)

    def perform_destroy(self, instance):
        filial = get_request_variable("filial")

        if filial is None:
            return super().perform_destroy(instance)

        merchant_id = filial.fl_merchat_id_ifood

        integrador = IntegradorProdutoIfood(merchant_id)
        integrador.excluir_registro_ifood(instance)

        return super().perform_destroy(instance) """

    def alterar_campos_unicos(self, instance):
        instance.pr_codigo_cardapio = gerar_codigo_cardapio()

    @action(methods=["get"], detail=False)
    def sugestao_codigo_cardapio(self, request):
        codigo = gerar_codigo_cardapio()
        return Response({"pr_codigo_cardapio": codigo})

    @action(methods=["put"], detail=True)
    def upload_imagem(self, request):
        produto = self.get_object()
        imagem = request.FILES.get("pr_imagem")
        Produto.upload(produto, imagem)
        return Response()


class CategoriaProdutoViewSet(BaseModelViewSet):
    queryset = CategoriaProduto.objects.all()
    serializer_class = CategoriaProdutoSerializer

    """ def perform_create(self, serializer, **overwrite):
        instance = super().perform_create(serializer, **overwrite)

        filial = get_request_variable("filial")

        if filial is None:
            return

        merchant_id = filial.fl_merchat_id_ifood
        catalog_id = filial.fl_catalog_id

        integrador = IntegradorCategoriasIfood(merchant_id, catalog_id)
        integrador.sincronizar_alteracoes_ifood(instance)

    def perform_update(self, serializer, **overwrite):
        instance = super().perform_update(serializer, **overwrite)

        filial = get_request_variable("filial")

        if filial is None:
            return

        merchant_id = filial.fl_merchat_id_ifood
        catalog_id = filial.fl_catalog_id

        integrador = IntegradorCategoriasIfood(merchant_id, catalog_id)
        integrador.sincronizar_alteracoes_ifood(instance)

    def perform_destroy(self, instance):
        filial = get_request_variable("filial")

        if filial is None:
            return super().perform_destroy(instance)

        merchant_id = filial.fl_merchat_id_ifood
        catalog_id = filial.fl_catalog_id

        integrador = IntegradorCategoriasIfood(merchant_id, catalog_id)
        integrador.deletar_categoria(instance)

        return super().perform_destroy(instance) """


# class ComplementoProdutoViewSet(BaseModelViewSet):
#     queryset = ComplementoProduto.objects.all()
#     serializer_classes = {
#         "list": ComplementoProdutoVisualizacaoSerializer,
#         "retrieve": ComplementoProdutoVisualizacaoSerializer,
#         "create": ComplementoProdutoAlteracaoSerializer,
#         "update": ComplementoProdutoAlteracaoSerializer,
#         "partial_update": ComplementoProdutoAlteracaoSerializer,
#         "bulk_create": ComplementoProdutoAlteracaoSerializer,
#         "clonar": ComplementoProdutoAlteracaoSerializer,
#     }


# class GrupoComplementoProdutoViewSet(BaseModelViewSet):
#     queryset = GrupoComplementoProduto.objects.all()
#     serializer_classes = {
#         "list": GrupoComplementoProdutoVisualizacaoSerializer,
#         "retrieve": GrupoComplementoProdutoVisualizacaoSerializer,
#         "create": GrupoComplementoProdutoAlteracaoSerializer,
#         "update": GrupoComplementoProdutoAlteracaoSerializer,
#         "partial_update": GrupoComplementoProdutoAlteracaoSerializer,
#         "bulk_create": GrupoComplementoProdutoAlteracaoSerializer,
#         "clonar": GrupoComplementoProdutoAlteracaoSerializer,
#     }


class CustomizacaoProdutoViewSet(BaseModelViewSet):
    queryset = CustomizacaoProduto.objects.all()
    serializer_classes = {
        "list": CustomizacaoProdutoVisualizacaoSerializer,
        "retrieve": CustomizacaoProdutoVisualizacaoSerializer,
        "create": CustomizacaoProdutoAlteracaoSerializer,
        "update": CustomizacaoProdutoAlteracaoSerializer,
        "partial_update": CustomizacaoProdutoAlteracaoSerializer,
        "bulk_create": CustomizacaoProdutoAlteracaoSerializer,
        "clonar": CustomizacaoProdutoAlteracaoSerializer,
    }


class CustomizacaoProdutoItemViewSet(BaseModelViewSet):
    queryset = CustomizacaoProdutoItem.objects.all()
    serializer_classes = {
        "list": CustomizacaoProdutoItemVisualizacaoSerializer,
        "retrieve": CustomizacaoProdutoItemVisualizacaoSerializer,
        "create": CustomizacaoProdutoItemAlteracaoSerializer,
        "update": CustomizacaoProdutoItemAlteracaoSerializer,
        "partial_update": CustomizacaoProdutoItemAlteracaoSerializer,
        "bulk_create": CustomizacaoProdutoItemAlteracaoSerializer,
        "clonar": CustomizacaoProdutoItemAlteracaoSerializer,
    }

    filterset_fields = {
        "cc_customizacao": ["exact"],
    }
