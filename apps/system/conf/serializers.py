from apps.system.base.serializers import (
    BaseModelSerializer,
    BaseModelSerializer,
)
from .models import Configuracao


class ConfiguracaoVisualizacaoSerializer(BaseModelSerializer):
    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr["cf_valor"] = Configuracao.normalize_value(
            repr["cf_codigo"], instance.cf_valor
        )
        return repr

    class Meta:
        model = Configuracao
        fields = "__all__"
        depth = 1


class ConfiguracaoAlteracaoSerializer(BaseModelSerializer):
    class Meta:
        model = Configuracao
        fields = "__all__"
