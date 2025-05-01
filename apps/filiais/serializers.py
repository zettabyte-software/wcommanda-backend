from apps.system.base.serializers import BaseModelSerializer

from .models import Filial


class FilialVisualizacaoSerializer(BaseModelSerializer):
    class Meta:
        model = Filial
        exclude = (
            "fl_client_secret_ifood",
            "fl_client_id_ifood",
            "fl_merchat_id_ifood",
            "fl_catalog_id",
            "fl_catalog_group_id",
        )
        # fields = "__all__"
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
