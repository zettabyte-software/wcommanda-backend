from apps.system.base.serializers import BaseModelSerializer

from .models import Assinatura, Plano


class AssinaturaVisualizacaoSerializer(BaseModelSerializer):
    class Meta:
        model = Assinatura
        fields = "__all__"
        depth = 1


class AssinaturaAlteracaoSerializer(BaseModelSerializer):
    class Meta:
        model = Assinatura
        fields = "__all__"


class PlanoVisualizacaoSerializer(BaseModelSerializer):
    class Meta:
        model = Plano
        fields = "__all__"
        depth = 1


class PlanoAlteracaoSerializer(BaseModelSerializer):
    class Meta:
        model = Plano
        fields = "__all__"
