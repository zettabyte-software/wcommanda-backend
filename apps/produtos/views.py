from rest_framework.decorators import action
from rest_framework.response import Response

from apps.ifood.integradores.categorias import IntegradorCategoriasIfood
from apps.system.base.views import BaseModelViewSet

from .serializers import (
    Acrescimo,
    AcrescimoAlteracaoSerializer,
    AcrescimoVisualizacaoSerializer,
    CategoriaProduto,
    CategoriaProdutoSerializer,
    GrupoComplementoProduto,
    GrupoComplementoProdutoAlteracaoSerializer,
    GrupoComplementoProdutoVisualizacaoSerializer,
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

    def perform_create(self, serializer, **overwrite):
        instance = super().perform_create(serializer, **overwrite)

        catalog_id = ""
        merchant_id = ""
        integrador = IntegradorCategoriasIfood(merchant_id, catalog_id)
        integrador.sincronizar_alteracoes_ifood(instance)

    def perform_update(self, serializer, **overwrite):
        instance = super().perform_update(serializer, **overwrite)

        catalog_id = ""
        merchant_id = ""
        integrador = IntegradorCategoriasIfood(merchant_id, catalog_id)
        integrador.sincronizar_alteracoes_ifood(instance)

    def perform_destroy(self, instance):
        catalog_id = ""
        merchant_id = ""
        integrador = IntegradorCategoriasIfood(merchant_id, catalog_id)
        integrador.deletar_categoria(instance)
        return super().perform_destroy(instance)

class AcrescimoViewSet(BaseModelViewSet):
    queryset = Acrescimo.objects.all()
    serializer_classes = {
        "list": AcrescimoVisualizacaoSerializer,
        "retrieve": AcrescimoVisualizacaoSerializer,
        "create": AcrescimoAlteracaoSerializer,
        "update": AcrescimoAlteracaoSerializer,
        "partial_update": AcrescimoAlteracaoSerializer,
        "bulk_create": AcrescimoAlteracaoSerializer,
        "clonar": AcrescimoAlteracaoSerializer,
    }


class GrupoComplementoProdutoViewSet(BaseModelViewSet):
    queryset = GrupoComplementoProduto.objects.all()
    serializer_classes = {
        "list": GrupoComplementoProdutoVisualizacaoSerializer,
        "retrieve": GrupoComplementoProdutoVisualizacaoSerializer,
        "create": GrupoComplementoProdutoAlteracaoSerializer,
        "update": GrupoComplementoProdutoAlteracaoSerializer,
        "partial_update": GrupoComplementoProdutoAlteracaoSerializer,
        "bulk_create": GrupoComplementoProdutoAlteracaoSerializer,
        "clonar": GrupoComplementoProdutoAlteracaoSerializer,
    }
