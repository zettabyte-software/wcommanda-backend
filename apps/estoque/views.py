from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet

from apps.system.base.views import BaseModelViewSet

from .serializers import (
    MovimentacaoEstoque,
    MovimentacaoEstoqueAlteracaoSerializer,
    MovimentacaoEstoqueVisualizacaoSerializer,
)
from .services import EstoqueProduto, criar_movimentacao


class MovimentacaoEstoqueViewSet(BaseModelViewSet):
    queryset = MovimentacaoEstoque.objects.all()
    serializer_classes = {
        "list": MovimentacaoEstoqueVisualizacaoSerializer,
        "retrieve": MovimentacaoEstoqueVisualizacaoSerializer,
        "create": MovimentacaoEstoqueAlteracaoSerializer,
        "update": MovimentacaoEstoqueAlteracaoSerializer,
        "partial_update": MovimentacaoEstoqueAlteracaoSerializer,
    }
    filterset_fields = {
        "id": ["icontains"],
        "mv_produto__pr_nome": ["icontains"],
        "mv_quantidade_atual": ["icontains"],
        "mv_quantidade": ["icontains"],
        "mv_quantidade_anterior": ["icontains"],
    }
    ordering_fields = [
        "id",
        "mv_produto__pr_nome",
        "mv_quantidade_atual",
        "mv_quantidade",
        "mv_quantidade_anterior",
    ]

    def perform_create(self, serializer):
        return criar_movimentacao(
            serializer.validated_data["mv_produto"],
            serializer.validated_data["mv_quantidade"],
            serializer.validated_data["mv_tipo"],
            serializer.validated_data.get("mv_comanda_item", None),
        )

class EstoqueAtualViewSet(GenericViewSet, ListModelMixin):
    queryset = MovimentacaoEstoque.objects.all()
    serializer_class = MovimentacaoEstoqueVisualizacaoSerializer

    def list(self, request):
        id_produto = request.query_params.get("mv_produto", None)
        queryset = EstoqueProduto.get_estoque_atual_produtos(id_produto)
        page = self.paginate_queryset(queryset)
        return self.get_paginated_response(page)
