from rest_framework import serializers

from apps.system.base.serializers import BaseModelSerializer

from .models import CategoriaProduto, ComplementoProduto, GrupoComplementoProduto, Produto


class CategoriaProdutoSerializer(BaseModelSerializer):
    class Meta:
        model = CategoriaProduto
        fields = "__all__"


class ProdutoVisualizacaoSerializer(BaseModelSerializer):
    pr_categoria = CategoriaProdutoSerializer()
    pr_url_imagem = serializers.SerializerMethodField(read_only=True)

    def get_pr_url_imagem(self, obj):
        return obj.pr_url_imagem

    class Meta:
        model = Produto
        exclude = (
            "pr_path_imagem",
            "pr_id_back_blaze",
        )


class ProdutoAlteracaoSerializer(BaseModelSerializer):
    pr_imagem = serializers.ImageField(write_only=True, required=False)

    def create(self, validated_data):
        imagem = validated_data.pop("pr_imagem", None)
        produto = Produto.objects.create(**validated_data)

        if imagem:
            Produto.upload(produto, imagem)

        return produto

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if 'pr_imagem' in self.initial_data:  # type: ignore
            imagem = validated_data.get('pr_imagem', None)
            if instance.pr_id_back_blaze and instance.pr_path_imagem:
                Produto.remover_foto(instance)

            if imagem is not None:
                Produto.upload(instance, imagem)

        return instance

    class Meta:
        model = Produto
        exclude = (
            "pr_path_imagem",
            "pr_id_back_blaze",
        )


class ComplementoProdutoVisualizacaoSerializer(BaseModelSerializer):
    class Meta:
        model = ComplementoProduto
        fields = "__all__"


class ComplementoProdutoAlteracaoSerializer(BaseModelSerializer):
    class Meta:
        model = ComplementoProduto
        fields = "__all__"


class GrupoComplementoProdutoVisualizacaoSerializer(BaseModelSerializer):
    class Meta:
        model = GrupoComplementoProduto
        fields = "__all__"


class GrupoComplementoProdutoAlteracaoSerializer(BaseModelSerializer):
    class Meta:
        model = GrupoComplementoProduto
        fields = "__all__"
