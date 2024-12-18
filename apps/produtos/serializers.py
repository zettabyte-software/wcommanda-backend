from apps.system.base.serializers import (
    BaseModelSerializer,
    BaseModelSerializer,
)
from .models import (
    CategoriaProduto,
    Produto,
)


class CategoriaProdutoSerializer(BaseModelSerializer):
    class Meta:
        model = CategoriaProduto
        fields = "__all__"


class ProdutoVisualizacaoSerializer(BaseModelSerializer):
    pr_categoria = CategoriaProdutoSerializer()

    class Meta:
        model = Produto
        fields = "__all__"


class ProdutoAlteracaoSerializer(BaseModelSerializer):
    def update(self, instance, validated_data):
        if "pr_imagem" in validated_data and validated_data["pr_imagem"] is None:
            instance.pr_imagem.delete(save=False)
            instance.pr_imagem = None
        return super().update(instance, validated_data)

    class Meta:
        model = Produto
        fields = "__all__"
