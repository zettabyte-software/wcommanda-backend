from apps.mesas.serializers import MesaVisualizacaoSerializer
from apps.system.base.serializers import BaseModelSerializer

from .models import Reserva


class ReservaVisualizacaoSerializer(BaseModelSerializer):
    rs_mesa = MesaVisualizacaoSerializer()

    class Meta:
        model = Reserva
        fields = "__all__"


class ReservaAlteracaoSerializer(BaseModelSerializer):
    class Meta:
        model = Reserva
        fields = "__all__"
