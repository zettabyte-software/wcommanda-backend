from rest_framework import serializers

from apps.system.base.serializers import BaseModelSerializer

from .models import (
    CatalogIfood,
    CategoriaIfood,
    PedidoIfood,
    PedidoItemComplementoIfood,
    PedidoItemIfood,
    ProdutoIfood,
)


class CatalogIfoodVisualizacaoSerializer(BaseModelSerializer):
    class Meta:
        model = CatalogIfood
        fields = "__all__"


class CatalogIfoodAlteracaoSerializer(BaseModelSerializer):
    class Meta:
        model = CatalogIfood
        fields = "__all__"


class CategoriaIfoodVisualizacaoSerializer(BaseModelSerializer):
    class Meta:
        model = CategoriaIfood
        fields = "__all__"


class CategoriaIfoodAlteracaoSerializer(BaseModelSerializer):
    class Meta:
        model = CategoriaIfood
        fields = "__all__"


class PedidoIfoodVisualizacaoSerializer(BaseModelSerializer):
    class Meta:
        model = PedidoIfood
        fields = "__all__"


class PedidoIfoodAlteracaoSerializer(BaseModelSerializer):
    class Meta:
        model = PedidoIfood
        fields = "__all__"


class PedidoItemComplementoIfoodVisualizacaoSerializer(BaseModelSerializer):
    class Meta:
        model = PedidoItemComplementoIfood
        fields = "__all__"


class PedidoItemComplementoIfoodAlteracaoSerializer(BaseModelSerializer):
    class Meta:
        model = PedidoItemComplementoIfood
        fields = "__all__"


class PedidoItemIfoodVisualizacaoSerializer(BaseModelSerializer):
    class Meta:
        model = PedidoItemIfood
        fields = "__all__"


class PedidoItemIfoodAlteracaoSerializer(BaseModelSerializer):
    class Meta:
        model = PedidoItemIfood
        fields = "__all__"


class ProdutoIfoodVisualizacaoSerializer(BaseModelSerializer):
    class Meta:
        model = ProdutoIfood
        fields = "__all__"


class ProdutoIfoodAlteracaoSerializer(BaseModelSerializer):
    class Meta:
        model = ProdutoIfood
        fields = "__all__"



class PedidoCancelamentoIfoodSerializer(serializers.Serializer):
    motivo = serializers.CharField()
