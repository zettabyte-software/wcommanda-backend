import logging

from apps.produtos.models import Produto
from apps.produtos.services import gerar_codigo_cardapio

from ..models import ProdutoIfood
from .base import BaseIntegradorIfood

logger = logging.getLogger(__name__)

LIMITE_REGISTROS = 100


class ImportadorProdutosIfoodMixin(BaseIntegradorIfood):
    def importar_produtos(self):
        produtos_ifood = self.get_produtos_ifood()
        for produto_ifood in produtos_ifood:
            restricoes_alimentares = produto_ifood["dietaryRestrictions"]
            produto_wcommanda = Produto.objects.create(
                pr_nome=produto_ifood["name"],
                pr_descricao=produto_ifood.get("description", "Produto integrado via iFood"),
                pr_codigo_cardapio=gerar_codigo_cardapio(),
                pr_vegano="VEGAN" in restricoes_alimentares,
                pr_vegetariano="VEGETARIAN" in restricoes_alimentares,
                pr_organico="ORGANIC" in restricoes_alimentares,
                pr_sem_gluten="GLUTEN_FREE" in restricoes_alimentares,
                pr_sem_acucar="SUGAR_FREE" in restricoes_alimentares,
                pr_zero_lactose="LACTOSE_FREE" in restricoes_alimentares,
            )

    def get_produtos_ifood(self):
        page = 1
        total_paginas = self.get_total_paginas_produtos()
        produtos = []

        while page <= total_paginas:
            produtos_pagina = self.get_produtos(page)
            produtos.extend(produtos_pagina)
            page += 1

        return produtos

    def get_produtos(self, page):
        response = self.client.get(
            f"catalog/v2.0/merchants/{self.merchant}/products?limit={LIMITE_REGISTROS}&page={page}"
        )
        response.raise_for_status()
        return response.json()["elements"]

    def get_total_paginas_produtos(self):
        response = self.client.get(f"catalog/v2.0/merchants/{self.merchant}/products?limit={LIMITE_REGISTROS}&page=1")
        dados = response.json()
        return dados["count"] // LIMITE_REGISTROS + 1


class IntegradorProdutoIfood(BaseIntegradorIfood):
    def sincronizar_alteracoes(self, produto: Produto):
        logger.info("Sincronizando alterações do produto %s no ifood", produto.pr_nome)
        logger.info("Alterações sincronizadas com sucesso para o produto %s", produto.pr_nome)

    def atualizar_inventario(self, produto: Produto, nova_quantidade: int):
        dados_ifood, _ = ProdutoIfood.objects.get_or_create(
            fd_produto=produto,
            defaults={
                "fd_produto": produto,
            },
        )
        dados = {"productId": dados_ifood.fd_ifood_id, "amount": nova_quantidade}
        response = self.client.get(f"/catalog/v2.0/merchants/{self.merchant}/inventory")
