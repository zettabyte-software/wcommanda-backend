from apps.system.base.views import BaseModelViewSet

from .serializers import (
    Assinatura,
    AssinaturaAlteracaoSerializer,
    AssinaturaVisualizacaoSerializer,
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
