from rest_framework import serializers

from apps.clientes.serializers import ClienteVisualizacaoSerializer
from apps.descontos.models import CuponDesconto
from apps.produtos.serializers import ProdutoVisualizacaoSerializer
from apps.system.base.serializers import BaseModelSerializer
from apps.system.conf.models import Configuracao

from .models import Comanda, ComandaItem, FormasPagamentoComandaChoices, StatusComandaChoices, StatusComandaItemChoices
from .services import baixar_estoque, vincular_num_pedido


class ComandaItemVisualizacaoSerializer(BaseModelSerializer):

    ct_produto = ProdutoVisualizacaoSerializer()
    ct_quantidade_total_produto = serializers.SerializerMethodField()
    ct_valor_total_produto = serializers.SerializerMethodField()

    def get_ct_quantidade_total_produto(self, obj: ComandaItem):
        """Utilizado no endpoint de visualização da comanda."""

        try:
            return obj.ct_quantidade_total_produto  # type: ignore
        except AttributeError:
            return 0

    def get_ct_valor_total_produto(self, obj: ComandaItem):
        """Utilizado no endpoint de visualização da comanda."""

        try:
            return obj.ct_valor_total_produto  # type: ignore
        except AttributeError:
            return 0

    class Meta:
        model = ComandaItem
        fields = "__all__"


class ComandaItemAlteracaoSerializer(BaseModelSerializer):
    def validate(self, attrs):
        validated_data = super().validate(attrs)
        if self.context["vincular_num_pedido"]:
            vincular_num_pedido(validated_data)
        return validated_data

    def create(self, validated_data):
        instance = super().create(validated_data)
        if instance.ct_produto.pr_status_padrao_comanda_item == StatusComandaItemChoices.ENTREGUE:
            baixar_estoque(instance)
        return instance

    class Meta:
        model = ComandaItem
        fields = "__all__"


class ComandaListSerializer(BaseModelSerializer):
    cm_valor_total = serializers.SerializerMethodField()

    def get_cm_valor_total(self, obj: Comanda):
        return obj.cm_valor_total

    class Meta:
        model = Comanda
        fields = "__all__"


class ComandaRetrieveSerializer(BaseModelSerializer):
    cm_itens = ComandaItemVisualizacaoSerializer(source="itens", many=True)
    cm_cliente_fidelidade = ClienteVisualizacaoSerializer()
    cm_valor_total = serializers.SerializerMethodField()

    def get_cm_valor_total(self, obj: Comanda):
        return obj.cm_valor_total

    class Meta:
        model = Comanda
        fields = "__all__"


class ComandaAlteracaoSerializer(BaseModelSerializer):
    class Meta:
        model = Comanda
        fields = "__all__"


class ComandaFinalizarSerializer(serializers.Serializer):
    cm_forma_pagamento = serializers.ChoiceField(choices=FormasPagamentoComandaChoices.choices)

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        comanda = self.context["comanda"]

        if comanda.cm_status != StatusComandaChoices.ABERTA:
            raise serializers.ValidationError({"mensagem": "Apenas uma comanda ABERTA pode ser finalizada"})

        controla_status_itens = Configuracao.get_configuracao("WCM_CONTROLE_STATUS_ITENS")

        if not controla_status_itens:
            itens = ComandaItem.objects.filter(ct_comanda=comanda).exclude(ct_status=StatusComandaItemChoices.PRONTO)

            for item in itens:
                baixar_estoque(item)

            itens.update(ct_status=StatusComandaItemChoices.PRONTO)
            return validated_data

        not_finished_status = (
            StatusComandaItemChoices.ABERTO,
            StatusComandaItemChoices.PREPARANDO,
            StatusComandaItemChoices.PRONTO,
        )

        itens = ComandaItem.objects.filter(ct_comanda=comanda)
        if itens.filter(ct_status__in=not_finished_status).exists():
            raise serializers.ValidationError(
                {"mensagem": "Finalize todos os itens para poder finalizar essa comanda"},
                "invalid_status",
            )

        return validated_data

    class Meta:
        fields = "__all__"


class ComandaCancelarSerializer(serializers.Serializer):
    cm_motivo = serializers.CharField(allow_blank=True)

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        comanda = self.context["comanda"]
        if comanda.cm_status != StatusComandaChoices.ABERTA:
            raise serializers.ValidationError({"mensagem": "Apenas uma comanda ABERTA pode ser cancelada"})
        return validated_data

    class Meta:
        fields = "__all__"


class AplicarCuponSerializer(serializers.Serializer):
    cupon = serializers.PrimaryKeyRelatedField(queryset=CuponDesconto.objects.all())

    def validate_cupon(self, cupon):
        if cupon.cp_utilizado:
            raise serializers.ValidationError({"mensagem": "Esse cupon já foi utilizado"})

        comanda = self.context["comanda"]

        try:
            cupon.get_valor_com_desconto(comanda.cm_valor_total)
        except ValueError as exc:
            raise serializers.ValidationError(
                {"mensagem": "A comanda não atende ao valor mínimo para aplicar o cupon "}
            ) from exc

        return cupon

    def save(self, **kwargs):
        data = self.validated_data

        cupon = data["cupon"]
        comanda = self.context["comanda"]

        comanda.cm_cupon = cupon
        comanda.save()
