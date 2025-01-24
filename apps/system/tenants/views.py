from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from django_multitenant.utils import set_current_tenant

from apps.system.base.views import BaseModelViewSet

from .serializers import Ambiente, AmbienteAlteracaoSerializer, AmbienteVisualizacaoSerializer, CriarAmbienteSerializer


class AmbienteViewSet(BaseModelViewSet):
    queryset = Ambiente.objects.all()
    serializer_classes = {
        "list": AmbienteVisualizacaoSerializer,
        "retrieve": AmbienteVisualizacaoSerializer,
        "create": AmbienteAlteracaoSerializer,
        "update": AmbienteAlteracaoSerializer,
        "partial_update": AmbienteAlteracaoSerializer,
    }

    def perform_create(self, serializer, **overwrite):
        set_current_tenant(None)
        return super().perform_create(serializer, **overwrite)


class CriarAssinaturaViewSet(ViewSet):
    permission_classes = [AllowAny]
    authentication_classes = []

    def create(self, request):
        set_current_tenant(None)
        serializer = CriarAmbienteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)
