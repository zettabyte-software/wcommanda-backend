from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from apps.system.conf.models import Configuracao

from .integradores.categorias import IntegradorCategoriasIfood
from .integrators import ImportarProdutosIfood, IntegradorPedidosIfood


class IfoodViewSet(ViewSet):
    @action(methods=["post"], detail=False)
    def webook(self, request):
        client_id = Configuracao.get_configuracao("WCM_CLIENT_ID_IFOOD")
        client_secret = Configuracao.get_configuracao("WCM_CLIENT_SECRET_IFOOD")

        if not client_id or not client_secret:
            return Response({"mensagem": "As credenciais do iFood não foram configuradas"}, status=status.HTTP_400_BAD_REQUEST)

        integrador = IntegradorPedidosIfood(client_id, client_secret, merchant="")

        integrador.criar_pedido_via_webhook(request.data)

        return Response(status=status.HTTP_202_ACCEPTED)

    @action(methods=["post"], detail=False)
    def importar_produtos_ifood(self, request):
        client_id = Configuracao.get_configuracao("WCM_CLIENT_ID_IFOOD")
        client_secret = Configuracao.get_configuracao("WCM_CLIENT_SECRET_IFOOD")

        if not client_id or not client_secret:
            return Response({"mensagem": "As credenciais do iFood não foram configuradas"}, status=status.HTTP_400_BAD_REQUEST)

        integrador = ImportarProdutosIfood(client_id, client_secret, merchant="")

        response = integrador.importar_produtos()

        return Response(response, status=status.HTTP_202_ACCEPTED)


    @action(methods=["post"], detail=False)
    def importar_categorias(self, request):
        client_id = Configuracao.get_configuracao("WCM_CLIENT_ID_IFOOD")
        client_secret = Configuracao.get_configuracao("WCM_CLIENT_SECRET_IFOOD")

        if not client_id or not client_secret:
            return Response({"mensagem": "As credenciais do iFood não foram configuradas"}, status=status.HTTP_400_BAD_REQUEST)

        integrador = IntegradorCategoriasIfood(client_id, client_secret, merchant="", catalog_id="")

        response = integrador.importar_categorias()

        return Response(response, status=status.HTTP_202_ACCEPTED)
