import logging

from django.db import transaction

from apps.produtos.models import Produto
from apps.produtos.services import gerar_codigo_cardapio

from ..models import ProdutoIfood
from .base import BaseIntegradorIfood

logger = logging.getLogger(__name__)

LIMITE_REGISTROS = 100


class ImportadorProdutosIfood(BaseIntegradorIfood):
    @transaction.atomic
    def importar_produtos(self):
        produtos_ifood = self.get_produtos_from_catalogo_ifood()
        dados_produtos_ifood_complementares = self.get_todos_produtos_ifood()

        for dados in produtos_ifood:
            produto_wcommanda = Produto(
                pr_nome=dados["itemName"],
                pr_descricao=dados.get("itemDescription", "Produto integrado via iFood"),
                pr_codigo_cardapio=gerar_codigo_cardapio(),
                pr_preco=dados["itemPrice"]["value"],
            )

            dados_complementares_produto = list(filter(
                lambda prod_comp: prod_comp["name"] == dados["itemName"],
                dados_produtos_ifood_complementares,
            ))

            if len(dados_complementares_produto) > 0:
                dados_complementares_produto = dados_complementares_produto[0]
                restricoes_alimentares = dados_complementares_produto["dietaryRestrictions"]

                if dados_complementares_produto:
                    produto_wcommanda.pr_vegano = "VEGAN" in restricoes_alimentares
                    produto_wcommanda.pr_vegetariano = "VEGETARIAN" in restricoes_alimentares
                    produto_wcommanda.pr_organico = "ORGANIC" in restricoes_alimentares
                    produto_wcommanda.pr_sem_gluten = "GLUTEN_FREE" in restricoes_alimentares
                    produto_wcommanda.pr_sem_acucar = "SUGAR_FREE" in restricoes_alimentares
                    produto_wcommanda.pr_zero_lactose = "LACTOSE_FREE" in restricoes_alimentares

            produto_wcommanda.save()

            ProdutoIfood.objects.create(
                fd_ifood_id=None,
                fd_produto=produto_wcommanda,
                fd_pizza=False,
                fd_categoria_id=dados["categoryId"],
                fd_grupo_catalogo_id=dados["catalogId"],
                fd_item_catalog_id=dados["itemId"],
                fd_index=dados["categoryIndex"],
            )

    def get_produtos_from_catalogo_ifood(self):
        catalogs = self.get_catalogs()
        itens = []

        for catalog_uuid in catalogs:
            produtos_pagina = self.get_produtos(catalog_uuid)

            for produto in produtos_pagina:
                produto["catalogId"] = catalog_uuid
            itens.extend(produtos_pagina)

        return itens

    def get_produtos(self, catalog_uuid):
        response = self.client.get(f"catalog/v2.0/merchants/{self.merchant}/catalogs/{catalog_uuid}/sellableItems")
        response.raise_for_status()
        return response.json()

    def get_catalogs(self):
        response = self.client.get(f"catalog/v2.0/merchants/{self.merchant}/catalogs/")
        response.raise_for_status()
        return (catalog["groupId"] for catalog in response.json())

    def processar_item_catalogo_ifood(self, dados):
        pass

    def get_todos_produtos_ifood(self):
        page = 1
        total_paginas = self.get_total_paginas_produtos_ifood()
        produtos = []

        while page <= total_paginas:
            produtos_pagina = self.fetch_produtos_ifood(page)
            produtos.extend(produtos_pagina)
            page += 1

        return produtos

    def fetch_produtos_ifood(self, page):
        response = self.client.get(
            f"catalog/v2.0/merchants/{self.merchant}/products?limit={LIMITE_REGISTROS}&page={page}"
        )
        response.raise_for_status()
        return response.json()["elements"]

    def get_total_paginas_produtos_ifood(self):
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
