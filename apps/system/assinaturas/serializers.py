from rest_framework import serializers

from apps.system.base.serializers import BaseModelSerializer
from apps.users.serializers import UsuarioSerializer

from .models import Assinatura, Plano
from .services import InicializadorAssinatura

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


class CriarAssinaturaSerializer(serializers.Serializer):
    assinatura = AssinaturaAlteracaoSerializer()
    usuario = UsuarioSerializer()

    def save(self, **kwargs):
        raise Exception
        manager = InicializadorAssinatura()
        manager.criar_assinatura(self.validated_data["assinatura"], self.validated_data["usuario"])  # type: ignore
