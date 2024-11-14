from apps.system.base.serializers import (
    BaseModelSerializer,
    BaseModelSerializer,
)

from .models import ComissaoGarcom


class ComissaoGarcomVisualizacaoSerializer(BaseModelSerializer):
    class Meta:
        model = ComissaoGarcom
        fields = "__all__"
        depth = 1


class ComissaoGarcomAlteracaoSerializer(BaseModelSerializer):
    class Meta:
        model = ComissaoGarcom
        fields = "__all__"
