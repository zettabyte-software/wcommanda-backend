from apps.system.base.serializers import (
    BaseModelSerializer,
)

from .models import Filial


class FilialVisualizacaoSerializer(BaseModelSerializer):
    class Meta:
        model = Filial
        fields = "__all__"
        depth = 1


class FilialAlteracaoSerializer(BaseModelSerializer):
    def update(self, instance, validated_data):
        if "fl_logo" in validated_data and validated_data["fl_logo"] is None:
            instance.fl_logo.delete(save=False)
            instance.fl_logo = None
        return super().update(instance, validated_data)

    class Meta:
        model = Filial
        fields = "__all__"
