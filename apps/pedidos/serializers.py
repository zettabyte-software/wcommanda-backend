from apps.system.base.serializers import BaseModelSerializer

from .models import Pedido, PedidoItem


class PedidoVisualizacaoSerializer(BaseModelSerializer):
    class Meta:
        model = Pedido
        fields = "__all__"


class PedidoAlteracaoSerializer(BaseModelSerializer):
    class Meta:
        model = Pedido
        fields = "__all__"


class PedidoItemVisualizacaoSerializer(BaseModelSerializer):
    class Meta:
        model = PedidoItem
        fields = "__all__"


class PedidoItemAlteracaoSerializer(BaseModelSerializer):
    class Meta:
        model = PedidoItem
        fields = "__all__"
