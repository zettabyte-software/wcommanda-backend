from apps.system.base.serializers import BaseModelSerializer

from .models import Fila


class FilaVisualizacaoSerializer(BaseModelSerializer):
    class Meta:
        model = Fila
        fields = "__all__"
        depth = 1


class FilaAlteracaoSerializer(BaseModelSerializer):
    class Meta:
        model = Fila
        fields = "__all__"
