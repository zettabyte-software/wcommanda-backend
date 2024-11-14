from apps.system.base.serializers import BaseModelSerializer

from .models import Ambiente


class AmbienteVisualizacaoSerializer(BaseModelSerializer):
    class Meta:
        model = Ambiente
        fields = "__all__"
        read_only_fields = ["mb_subdominio", "mb_nome"]


class AmbienteAlteracaoSerializer(BaseModelSerializer):
    class Meta:
        model = Ambiente
        fields = "__all__"
