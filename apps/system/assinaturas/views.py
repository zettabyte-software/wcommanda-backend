from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from django_multitenant.utils import set_current_tenant

from apps.system.base.views import BaseModelViewSet

from .serializers import (
    Assinatura,
    AssinaturaAlteracaoSerializer,
    AssinaturaVisualizacaoSerializer,
    CriarAssinaturaSerializer,
    Plano,
    PlanoAlteracaoSerializer,
    PlanoVisualizacaoSerializer,
)


class AssinaturaViewSet(BaseModelViewSet):
    queryset = Assinatura.objects.all()
    serializer_classes = {
        "list": AssinaturaVisualizacaoSerializer,
        "retrieve": AssinaturaVisualizacaoSerializer,
        "create": AssinaturaAlteracaoSerializer,
        "update": AssinaturaAlteracaoSerializer,
        "partial_update": AssinaturaAlteracaoSerializer,
        "bulk_create": AssinaturaAlteracaoSerializer,
    }


class PlanoViewSet(BaseModelViewSet):
    queryset = Plano.objects.all()
    serializer_classes = {
        "list": PlanoVisualizacaoSerializer,
        "retrieve": PlanoVisualizacaoSerializer,
        "create": PlanoAlteracaoSerializer,
        "update": PlanoAlteracaoSerializer,
        "partial_update": PlanoAlteracaoSerializer,
        "bulk_create": PlanoAlteracaoSerializer,
    }


class CriarAssinaturaViewSet(ViewSet):
    permission_classes = [AllowAny]
    authentication_classes = []

    def create(self, request):
        set_current_tenant(None)
        serializer = CriarAssinaturaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)
