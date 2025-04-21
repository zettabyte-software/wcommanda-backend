import logging

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ReadOnlyModelViewSet

from threadlocals.threadlocals import get_request_variable

from .authentications import IFoodWebhookAuthentication
from .integradores.categorias import IntegradorCategoriasIfood
from .integradores.pedidos import IntegradorPedidosIfood
from .integradores.produtos import ImportadorProdutosIfood
from .serializers import PedidoCancelamentoIfoodSerializer, PedidoIfood, PedidoIfoodVisualizacaoSerializer

logger = logging.getLogger(__name__)


class PedidoIfoodViewSet(ReadOnlyModelViewSet):
    authentication_classes = [IFoodWebhookAuthentication]
    permission_classes  = [AllowAny]
    queryset = PedidoIfood.objects.filter(ativo=True)
    serializer_class = PedidoIfoodVisualizacaoSerializer

    @action(methods=["post"], detail=False)
    def webhook(self, request: Request):
        # print(request.data)
        # print(request.headers)
        # client_secret = Configuracao.get_configuracao("WCM_CLIENT_SECRET_IFOOD")
        # signature = request.headers.get("X-Ifood-Signature", None)

        # evento_valido = WebhookPedidoIfood.validar_evento_ifood(request.data, signature, client_secret)

        # logger.info("evento_valido: %s", evento_valido)
        # logger.info("client_secret: %s", client_secret)
        # logger.info("signature: %s", signature)

        # integrador = WebhookPedidoIfood(filial.fl_merchat_id_ifood)
        # integrador.criar_pedido_via_webhook(request.data)

        return Response()

    @action(methods=["post"], detail=True)
    def confirmar(self, request: Request, pk: int):
        filial = get_request_variable("filial")

        if not filial:
            return Response({"mensagem": "ERRO"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        pedido = self.get_object()
        integrador = IntegradorPedidosIfood(filial.fl_merchat_id_ifood)
        status_integracao, _ = integrador.confirmar(pedido.fd_ifood_id)
        return Response(status=status_integracao)

    @action(methods=["post"], detail=True)
    def iniciar_preparacao(self, request: Request, pk: int):
        filial = get_request_variable("filial")

        if not filial:
            return Response({"mensagem": "ERRO"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        pedido = self.get_object()
        integrador = IntegradorPedidosIfood(filial.fl_merchat_id_ifood)
        status_integracao, _ = integrador.iniciar_preparacao(pedido.fd_ifood_id)
        return Response(status=status_integracao)

    @action(methods=["post"], detail=True)
    def preparar_recebimento(self, request: Request, pk: int):
        filial = get_request_variable("filial")

        if not filial:
            return Response({"mensagem": "ERRO"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        pedido = self.get_object()
        integrador = IntegradorPedidosIfood(filial.fl_merchat_id_ifood)
        status_integracao, _ = integrador.preparar_recebimento(pedido.fd_ifood_id)
        return Response(status=status_integracao)

    @action(methods=["post"], detail=True)
    def dispachar(self, request: Request, pk: int):
        filial = get_request_variable("filial")

        if not filial:
            return Response({"mensagem": "ERRO"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        pedido = self.get_object()
        integrador = IntegradorPedidosIfood(filial.fl_merchat_id_ifood)
        status_integracao, _ = integrador.dispachar(pedido.fd_ifood_id)
        return Response(status=status_integracao)

    @action(methods=["post"], detail=True)
    def cancelar(self, request: Request, pk: int):
        filial = get_request_variable("filial")

        if not filial:
            return Response({"mensagem": "ERRO"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        pedido = self.get_object()
        serializer = PedidoCancelamentoIfoodSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        integrador = IntegradorPedidosIfood(filial.fl_merchat_id_ifood)
        status_integracao, _ = integrador.solicitar_cancelamento(pedido.fd_ifood_id, serializer.validated_data["motivo"])
        return Response(status=status_integracao)

    @action(methods=["post"], detail=True)
    def solicitar_cancelamento(self, request: Request, pk: int):
        filial = get_request_variable("filial")

        if not filial:
            return Response({"mensagem": "ERRO"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        pedido = self.get_object()
        integrador = IntegradorPedidosIfood(filial.fl_merchat_id_ifood)
        status_integracao, _ = integrador.solicitar_cancelamento(pedido.fd_ifood_id)
        return Response(status=status_integracao)


class IntegracaoIfoodViewSet(GenericViewSet):
    @action(methods=["post"], detail=False)
    def produtos(self, request: Request):
        filial = get_request_variable("filial")

        if not filial:
            return Response({"mensagem": "ERRO"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        integrador = ImportadorProdutosIfood(filial.fl_merchat_id_ifood)
        response = integrador.importar_produtos()
        return Response(response)

    @action(methods=["post"], detail=False)
    def categorias(self, request: Request):
        filial = get_request_variable("filial")

        if not filial:
            return Response({"mensagem": "ERRO"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        integrador = IntegradorCategoriasIfood(filial.fl_merchat_id_ifood, filial.fl_catalog_grupo_id)
        response = integrador.importar_categorias()
        return Response(response)
