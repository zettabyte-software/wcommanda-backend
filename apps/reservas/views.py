from apps.system.base.views import BaseModelViewSet

from .serializers import (
    Reserva,
    ReservaAlteracaoSerializer,
    ReservaVisualizacaoSerializer,
)


class ReservaViewSet(BaseModelViewSet):
    queryset = Reserva.objects.all()
    serializer_classes = {
        "list": ReservaVisualizacaoSerializer,
        "retrieve": ReservaVisualizacaoSerializer,
        "create": ReservaAlteracaoSerializer,
        "update": ReservaAlteracaoSerializer,
        "partial_update": ReservaAlteracaoSerializer,
        "bulk_create": ReservaAlteracaoSerializer,
    }
