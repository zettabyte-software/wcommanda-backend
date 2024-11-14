from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from apps.system.base.serializers import BaseModelSerializer
from apps.system.core.classes import Email

from .models import Carimbo, CartaoFidelidade, CondicaoPremio, Premio, PremioItem


class PremioItemVisualizacaoSerializer(BaseModelSerializer):
    class Meta:
        model = PremioItem
        fields = "__all__"
        depth = 1


class PremioItemAlteracaoSerializer(BaseModelSerializer):
    class Meta:
        model = PremioItem
        fields = "__all__"


class PremioVisualizacaoSerializer(BaseModelSerializer):
    def __init__(self, instance=None, data=serializers.empty, **kwargs):
        super().__init__(instance, data, **kwargs)

        if self.context["action"] == "retrieve":
            self.fields["pm_itens"] = PremioItemVisualizacaoSerializer(source="itens", many=True)

    class Meta:
        model = Premio
        fields = "__all__"
        depth = 1


class PremioAlteracaoSerializer(BaseModelSerializer):
    class Meta:
        model = Premio
        fields = "__all__"


class CartaoFidelidadeVisualizacaoSerializer(BaseModelSerializer):
    cr_total_carimbos = serializers.SerializerMethodField()
    cr_expirado = serializers.SerializerMethodField()

    def get_cr_expirado(self, obj):
        return obj.cr_expirado

    def get_cr_total_carimbos(self, obj):
        return obj.cr_total_carimbos

    class Meta:
        model = CartaoFidelidade
        fields = "__all__"
        depth = 1


class CartaoFidelidadeAlteracaoSerializer(BaseModelSerializer):
    class Meta:
        model = CartaoFidelidade
        fields = "__all__"


class CarimboVisualizacaoSerializer(BaseModelSerializer):
    class Meta:
        model = Carimbo
        fields = "__all__"
        depth = 1


class CarimboAlteracaoSerializer(BaseModelSerializer):
    class Meta:
        model = Carimbo
        fields = "__all__"


class CondicaoPremioVisualizacaoSerializer(BaseModelSerializer):
    class Meta:
        model = CondicaoPremio
        fields = "__all__"
        depth = 1


class CondicaoPremioAlteracaoSerializer(BaseModelSerializer):
    class Meta:
        model = CondicaoPremio
        fields = "__all__"


class EnviarLinkCartaoFidelidadeSerializer(serializers.Serializer):
    cartao_fidelidade = serializers.PrimaryKeyRelatedField(queryset=CartaoFidelidade.objects.all())

    def validate_cartao_fidelidade(self, value):
        if value.cr_expirado:
            raise serializers.ValidationError(_("Esse cartão fidelidade já venceu e não pode ser reenviada ao cliente"))

        if value.cr_status == CartaoFidelidade.OPCOES_STATUS.CANCELADA:
            raise serializers.ValidationError(_("Não é possível enviar um cartão fidelidade que já foi cancelado"))

        if not value.cr_cliente.cl_email:
            raise serializers.ValidationError(_("O cliente não possui um email informado"))

        return value

    def save(self, **kwargs):
        data = self.validated_data

        cartao_fidelidade = data["cartao_fidelidade"]

        email = Email(
            titulo=f"Cartão Fidelidade wCommanda | {cartao_fidelidade.cr_filial.fl_nome}",
            corpo=f"Clique no link abaixo para acessar seu cartão fidelidade: {cartao_fidelidade.cr_link}",
            destinatarios=[cartao_fidelidade.cr_cliente.cl_email],
        )

        email.send()
