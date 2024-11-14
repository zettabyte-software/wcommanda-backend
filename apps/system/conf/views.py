from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.system.base.views import BaseModelViewSet
from apps.system.core.records import DefaultRecordsManger

from .serializers import (
    Configuracao,
    ConfiguracaoVisualizacaoSerializer,
    ConfiguracaoAlteracaoSerializer,
)


class ConfiguracaoViewSet(BaseModelViewSet):
    queryset = Configuracao.objects.all()
    serializer_classes = {
        "list": ConfiguracaoVisualizacaoSerializer,
        "retrieve": ConfiguracaoVisualizacaoSerializer,
        "create": ConfiguracaoAlteracaoSerializer,
        "update": ConfiguracaoAlteracaoSerializer,
        "partial_update": ConfiguracaoAlteracaoSerializer,
    }
    filterset_fields = {
        "cf_codigo": ["exact", "icontains"],
    }

    def create(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(methods=["get"], detail=False)
    def criar_registros_padrao(self, request, *args, **kwargs):
        manager = DefaultRecordsManger()
        manager.apply_updates()
        return Response()
