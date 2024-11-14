from apps.system.base.serializers import (
    BaseModelSerializer,
)
from .models import Mesa


class MesaVisualizacaoSerializer(BaseModelSerializer):
    class Meta:
        model = Mesa
        fields = "__all__"
        depth = 1


class MesaAlteracaoSerializer(BaseModelSerializer):
    class Meta:
        model = Mesa
        fields = "__all__"
