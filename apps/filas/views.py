from django.utils.translation import gettext_lazy as _

from rest_framework.decorators import action
from rest_framework.response import Response

from apps.system.base.views import BaseModelViewSet
from lib.twilio.sms import TwilioSmsHandler

from .serializers import (
    Fila,
    FilaAlteracaoSerializer,
    FilaVisualizacaoSerializer,
)

MENSAGEM_PADRAO_FIM_ESPERA = _("ATENÇÂO: SUA VEZ NA FILA DE ESPERA DO NOME_RESTAURANTE CHEGOU")


class FilaViewSet(BaseModelViewSet):
    queryset = Fila.objects.all()
    serializer_classes = {
        "list": FilaVisualizacaoSerializer,
        "retrieve": FilaVisualizacaoSerializer,
        "create": FilaAlteracaoSerializer,
        "update": FilaAlteracaoSerializer,
        "partial_update": FilaAlteracaoSerializer,
        "bulk_create": FilaAlteracaoSerializer,
    }

    @action(detail=True, methods=["post"])
    def enviar_sms_liberacao(self, request):
        instance = self.get_object()
        handler = TwilioSmsHandler()
        handler.enviar_sms(instance.ff_telefone, MENSAGEM_PADRAO_FIM_ESPERA)
        return Response()

    @action(detail=True, methods=["post"])
    def confirmar_entrada(self, request):
        instance = self.get_object()
        Fila.receber_pessoas(instance.ff_posicao)
        return Response()

    @action(detail=True, methods=["post"])
    def remover_pessoa(self, request):
        instance = self.get_object()
        Fila.remover_pessoa(instance.pk)
        return Response()
