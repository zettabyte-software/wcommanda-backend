from django.utils import timezone

from rest_framework import serializers

from apps.clientes.models import Cliente
from apps.system.base.serializers import (
    BaseModelSerializer,
)

from .models import CuponDesconto, TiposDescontoChoices


class CuponDescontoVisualizacaoSerializer(BaseModelSerializer):
    class Meta:
        model = CuponDesconto
        fields = "__all__"
        depth = 1


class CuponDescontoAlteracaoSerializer(BaseModelSerializer):
    class Meta:
        model = CuponDesconto
        fields = "__all__"


class GerarCuponAniversarioSerializer(serializers.Serializer):
    tipo_desconto = serializers.ChoiceField(choices=TiposDescontoChoices.choices)
    valor_desconto = serializers.IntegerField()
    cliente = serializers.PrimaryKeyRelatedField(queryset=Cliente.objects.all())

    def validate_cliente(self, cliente):
        if cliente.cl_nascimento != timezone.now().date():
            raise serializers.ValidationError({"mensagem": f"Hoje não é o aniversário de {cliente.cl_nome} {cliente.cl_sobrenome}"})
        return cliente

    def save(self, **kwargs):
        data = self.validated_data

        cupon = CuponDesconto.objects.create(
            cp_tipo=data["tipo_desconto"],
            cp_expiracao=timezone.now(),
            cp_valor=data["valor_desconto"],
            cp_valor_minimo=0,
        )

        return cupon
