from apps.system.base.views import BaseModelViewSet

from .serializers import (
    Fila,
    FilaAlteracaoSerializer,
    FilaVisualizacaoSerializer,
)


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
