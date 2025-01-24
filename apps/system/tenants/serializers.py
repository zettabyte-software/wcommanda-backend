from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from apps.system.base.serializers import BaseModelSerializer
from apps.users.serializers import UsuarioSerializer

from .models import Ambiente
from .services import TenantManager


class AmbienteVisualizacaoSerializer(BaseModelSerializer):
    class Meta:
        model = Ambiente
        fields = "__all__"
        read_only_fields = ["mb_subdominio", "mb_nome"]


class AmbienteAlteracaoSerializer(BaseModelSerializer):
    class Meta:
        model = Ambiente
        fields = "__all__"


class CriarAmbienteSerializer(serializers.Serializer):
    ambiente = AmbienteAlteracaoSerializer()
    usuario = UsuarioSerializer()

    def save(self, **kwargs):
        manager = TenantManager()
        manager.criar_tenant(self.validated_data["ambiente"], self.validated_data["usuario"])  # type: ignore
