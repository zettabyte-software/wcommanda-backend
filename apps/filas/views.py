from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.system.base.views import BaseModelViewSet
from lib.twilio.sms import TwilioSmsHandler

from .messages import MENSAGEM_FILA_ESPERA
from .serializers import (
    Fila,
    FilaAlteracaoSerializer,
    FilaVisualizacaoSerializer,
)


class FilaViewSet(BaseModelViewSet):
    queryset = Fila.objects.all().order_by("ff_posicao")
    serializer_classes = {
        "list": FilaVisualizacaoSerializer,
        "retrieve": FilaVisualizacaoSerializer,
        "create": FilaAlteracaoSerializer,
        "update": FilaAlteracaoSerializer,
        "partial_update": FilaAlteracaoSerializer,
        "bulk_create": FilaAlteracaoSerializer,
    }

    @action(detail=True, methods=["post"])
    def enviar_sms_liberacao(self, request, pk):
        instance = self.get_object()
        handler = TwilioSmsHandler()
        handler.enviar_sms(instance.ff_celular, MENSAGEM_FILA_ESPERA)
        return Response()

    @action(detail=True, methods=["post"])
    def confirmar_entrada(self, request, pk):
        instance = self.get_object()
        Fila.receber_pessoas(instance.ff_posicao)
        return Response()

    @action(detail=True, methods=["post"])
    def remover_pessoa(self, request, pk):
        instance = self.get_object()
        Fila.remover_pessoa(instance.pk)
        return Response()


class FilaEsperaClienteViewSet(GenericViewSet):
    authentication_classes = []
    permission_classes = []

    def retrieve(self, request, pk):
        posicao_fila = get_object_or_404(Fila, pk=pk)
        serializer = FilaVisualizacaoSerializer(posicao_fila)
        return Response(serializer.data)
