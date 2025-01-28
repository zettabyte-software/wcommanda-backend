from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from threadlocals.threadlocals import get_request_variable

from apps.system.base.views import BaseViewSet

from .integradores.categorias import IntegradorCategoriasIfood
from .integradores.pedidos import IntegradorPedidosIfood
from .integradores.produtos import ImportadorProdutosIfood
from .serializers import PedidoIfood, PedidoIfoodVisualizacaoSerializer


class IfoodViewSet(BaseViewSet):
    queryset = PedidoIfood.objects.filter(ativo=True)

    @action(methods=["get"], detail=False)
    def pedidos_integrados(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        serializer = PedidoIfoodVisualizacaoSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(methods=["post"], detail=False)
    def webhook(self, request):
        filial = get_request_variable("filial")

        if not filial:
            return Response({"mensagem": "ERRO"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        integrador = IntegradorPedidosIfood(filial.fl_merchat_id_ifood)
        integrador.criar_pedido_via_webhook(request.data)

        return Response()

    @action(methods=["post"], detail=False)
    def importar_produtos_ifood(self, request):
        filial = get_request_variable("filial")

        if not filial:
            return Response({"mensagem": "ERRO"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        integrador = ImportadorProdutosIfood(filial.fl_merchat_id_ifood)

        response = integrador.importar_produtos()

        return Response(response)

    @action(methods=["post"], detail=False)
    def importar_categorias(self, request):
        filial = get_request_variable("filial")

        if not filial:
            return Response({"mensagem": "ERRO"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        integrador = IntegradorCategoriasIfood(filial.fl_merchat_id_ifood, filial.fl_catalogo_grupo_id)

        response = integrador.importar_categorias()

        return Response(response)
