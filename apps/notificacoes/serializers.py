from apps.system.base.serializers import BaseModelSerializer

from .models import Notificacao


class NotificacaoVisualizacaoSerializer(BaseModelSerializer):
    class Meta:
        model = Notificacao
        fields = "__all__"


class NotificacaoAlteracaoSerializer(BaseModelSerializer):
    class Meta:
        model = Notificacao
        fields = "__all__"
