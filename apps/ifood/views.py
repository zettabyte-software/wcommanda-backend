from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from threadlocals.threadlocals import get_request_variable

from .integradores.categorias import IntegradorCategoriasIfood
from .integradores.pedidos import IntegradorPedidosIfood
from .integradores.produtos import ImportadorProdutosIfood


class IfoodViewSet(ViewSet):
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
