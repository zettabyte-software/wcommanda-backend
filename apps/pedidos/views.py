from apps.system.base.views import BaseModelViewSet

from .serializers import (
    Pedido,
    PedidoAlteracaoSerializer,
    PedidoItem,
    PedidoItemAlteracaoSerializer,
    PedidoItemVisualizacaoSerializer,
    PedidoVisualizacaoSerializer,
)


class PedidoViewSet(BaseModelViewSet):
    queryset = Pedido.objects.all()
    serializer_classes = {
        "list": PedidoVisualizacaoSerializer,
        "retrieve": PedidoVisualizacaoSerializer,
        "create": PedidoAlteracaoSerializer,
        "update": PedidoAlteracaoSerializer,
        "partial_update": PedidoAlteracaoSerializer,
    }


class PedidoItemViewSet(BaseModelViewSet):
    queryset = PedidoItem.objects.all()
    serializer_classes = {
        "list": PedidoItemVisualizacaoSerializer,
        "retrieve": PedidoItemVisualizacaoSerializer,
        "create": PedidoItemAlteracaoSerializer,
        "update": PedidoItemAlteracaoSerializer,
        "partial_update": PedidoItemAlteracaoSerializer,
    }
