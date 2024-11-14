from apps.system.base.serializers import BaseModelSerializer

from .models import MovimentacaoEstoque


class MovimentacaoEstoqueVisualizacaoSerializer(BaseModelSerializer):
    class Meta:
        model = MovimentacaoEstoque
        fields = "__all__"
        depth = 3


class MovimentacaoEstoqueAlteracaoSerializer(BaseModelSerializer):
    class Meta:
        model = MovimentacaoEstoque
        fields = "__all__"
