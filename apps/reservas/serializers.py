from apps.system.base.serializers import BaseModelSerializer

from .models import Reserva


class ReservaVisualizacaoSerializer(BaseModelSerializer):
    class Meta:
        model = Reserva
        fields = "__all__"


class ReservaAlteracaoSerializer(BaseModelSerializer):
    class Meta:
        model = Reserva
        fields = "__all__"
