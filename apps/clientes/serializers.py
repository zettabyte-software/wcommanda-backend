from apps.system.base.serializers import BaseModelSerializer

from .models import Cliente


class ClienteVisualizacaoSerializer(BaseModelSerializer):
    class Meta:
        model = Cliente
        fields = "__all__"
        depth = 1


class ClienteAlteracaoSerializer(BaseModelSerializer):
    class Meta:
        model = Cliente
        fields = "__all__"
