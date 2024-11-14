from django.utils import timezone

from apps.comandas.models import ComandaItem, StatusComandaItemChoices
from apps.produtos.serializers import Produto

from .models import MovimentacaoEstoque


class EstoqueProduto:
    def __init__(self, produto) -> None:
        self.produto = produto

    @property
    def quantidade_disponivel(self):
        """Calcula a quantidade disponível de um item em estoque.

        Returns:
                float: A quantidade total disponível, calculada subtraindo a quantidade reservada da quantidade total.

        """
        return self.quantidade_total - self.quantidade_reservada

    @property
    def quantidade_total(self):
        """Calcula a quantidade total de um produto em estoque.

        Busca a primeira movimentação de estoque associada ao produto e retorna sua quantidade atual.
        Se não houver movimentação registrada, retorna 0.

        Returns:
            float: Quantidade atual do produto em estoque

        """
        movimentacao = MovimentacaoEstoque.objects.filter(mv_produto=self.produto).first()
        if movimentacao:
            return movimentacao.mv_quantidade_atual

        return 0

    @property
    def quantidade_reservada(self):
        """Retorna a quantidade de produtos reservados em comandas, mas ainda não entregues.

        A quantidade é calculada com base no número de instâncias de ComandaItem criadas hoje
        que estão associadas ao produto atual e têm status de 'ABERTO', 'PREPARANDO' ou 'PRONTO'.

        Retorna:
            int: O número de produtos reservados.
        """

        """Quantidade de produtos reservados em comandas, mas ainda não entregues."""
        quantidade = ComandaItem.objects.filter(
            data_criacao=timezone.now().date(),
            ct_produto=self.produto,
            ct_status__in=(
                StatusComandaItemChoices.ABERTO,
                StatusComandaItemChoices.PREPARANDO,
                StatusComandaItemChoices.PRONTO,
            ),
        ).count()

        return quantidade

    @classmethod
    def get_estoque_atual_produtos(cls, id_produtos=None):
        """Recupera as informações atuais de estoque para produtos que controlam estoque.

        Args:
            id_produtos (list, opcional): Uma lista de IDs de produtos para filtrar as informações de estoque.
                                        Se não fornecido, recupera informações de estoque para todos os produtos que controlam estoque.

        Returns:
            list: Uma lista de dicionários contendo informações de estoque para cada produto. Cada dicionário contém:
                - "mv_produto" (str): O nome do produto.
                - "mv_quantidade_atual" (int): A quantidade disponível atual do produto.
                - "mv_quantidade_reservada" (float): A quantidade reservada do produto.
                - "mv_quantidade_real" (int): A quantidade total do produto.

        """
        produtos = Produto.objects.filter(pr_controla_estoque=True)

        if id_produtos:
            produtos = produtos.filter(id__in=id_produtos)

        dados_estoque = []
        estoque_produtos = [EstoqueProduto(produto) for produto in produtos]
        for estoque in estoque_produtos:
            dados_estoque.append(
                {
                    "mv_produto": estoque.produto.pr_nome,
                    "mv_quantidade_atual": estoque.quantidade_disponivel,
                    "mv_quantidade_reservada": float(estoque.quantidade_reservada),
                    "mv_quantidade_real": estoque.quantidade_total,
                }
            )

        return dados_estoque
