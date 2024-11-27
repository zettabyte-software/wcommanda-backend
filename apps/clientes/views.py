from apps.system.base.views import BaseModelViewSet

from .serializers import (
    Cliente,
    ClienteAlteracaoSerializer,
    ClienteVisualizacaoSerializer,
)


class ClienteViewSet(BaseModelViewSet):
    queryset = Cliente.objects.all()
    serializer_classes = {
        "list": ClienteVisualizacaoSerializer,
        "retrieve": ClienteVisualizacaoSerializer,
        "create": ClienteAlteracaoSerializer,
        "update": ClienteAlteracaoSerializer,
        "partial_update": ClienteAlteracaoSerializer,
        "bulk_create": ClienteAlteracaoSerializer,
    }
    filterset_fields = {
        "id": ["exact", "icontains"],
        "cl_nome": ["exact", "icontains"],
        "cl_celular": ["exact", "icontains"],
        "cl_telefone": ["exact", "icontains"],
        "cl_email": ["exact", "icontains"],
    }
