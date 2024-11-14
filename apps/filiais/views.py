from apps.system.base.views import BaseModelViewSet

from .serializers import (
    Filial,
    FilialVisualizacaoSerializer,
    FilialAlteracaoSerializer,
)


class FilialViewSet(BaseModelViewSet):
    queryset = Filial.objects.all()
    serializer_classes = {
        "list": FilialVisualizacaoSerializer,
        "retrieve": FilialVisualizacaoSerializer,
        "create": FilialAlteracaoSerializer,
        "update": FilialAlteracaoSerializer,
        "partial_update": FilialAlteracaoSerializer,
    }
    filterset_fields = {
        "fl_nome": ["exact", "icontains"],
    }
