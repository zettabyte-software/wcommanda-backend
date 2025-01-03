import dataclasses
import logging

from django.db import transaction

from apps.produtos.models import Produto
from apps.produtos.services import gerar_codigo_cardapio

from ..models import ProdutoIfood
from .base import BaseIntegradorIfood, IntegradorCadastroIfood

logger = logging.getLogger(__name__)

LIMITE_REGISTROS = 100


@dataclasses.dataclass
class ProdutoIfoodDataclass:
    id: str
    name: str
    image: str
    shifts: list
    serving: str
    dietaryRestrictions: list
    weight: dict


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

            dados_complementares_produto = list(
                filter(
                    lambda prod_comp: prod_comp["name"] == dados["itemName"],
                    dados_produtos_ifood_complementares,
                )
            )

            id_ifood = None

            if len(dados_complementares_produto) > 0:
                dados_complementares_produto = dados_complementares_produto[0]

                if dados_complementares_produto:
                    restricoes_alimentares = dados_complementares_produto["dietaryRestrictions"]

                    produto_wcommanda.pr_vegano = "VEGAN" in restricoes_alimentares
                    produto_wcommanda.pr_vegetariano = "VEGETARIAN" in restricoes_alimentares
                    produto_wcommanda.pr_organico = "ORGANIC" in restricoes_alimentares
                    produto_wcommanda.pr_sem_gluten = "GLUTEN_FREE" in restricoes_alimentares
                    produto_wcommanda.pr_sem_acucar = "SUGAR_FREE" in restricoes_alimentares
                    produto_wcommanda.pr_zero_lactose = "LACTOSE_FREE" in restricoes_alimentares

                    id_ifood = dados_complementares_produto["id"]

            produto_wcommanda.save()

            ProdutoIfood.objects.create(
                fd_ifood_id=id_ifood,
                fd_produto=produto_wcommanda,
                fd_pizza=False,
                fd_categoria_id=dados["categoryId"],
                fd_grupo_catalogo_id=dados["catalogId"],
                fd_item_catalogo_id=dados["itemId"],
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

    def fetch_produtos_ifood(self, page: int):
        response = self.client.get(
            f"catalog/v2.0/merchants/{self.merchant}/products?limit={LIMITE_REGISTROS}&page={page}"
        )
        response.raise_for_status()
        return response.json()["elements"]

    def get_total_paginas_produtos_ifood(self):
        response = self.client.get(f"catalog/v2.0/merchants/{self.merchant}/products?limit={LIMITE_REGISTROS}&page=1")
        dados = response.json()
        return dados["count"] // LIMITE_REGISTROS + 1


class IntegradorProdutoIfood(IntegradorCadastroIfood):
    def criar_registro_ifood(self, instance, dados):
        url = f"catalog/v2.0/merchants/{self.merchant}/products"
        response = self.client.post(url, json=dados)
        response.raise_for_status()
        dados_ifood = ProdutoIfoodDataclass(**response.json())
        self.atualizar_dados_internos(instance, dados_ifood)
        return response

    def atualizar_registro_ifood(self, instance, dados, id_ifood):
        url = f"catalog/v2.0/merchants/{self.merchant}/products/{id_ifood}"
        response = self.client.post(url, json=dados)
        response.raise_for_status()
        dados_ifood = ProdutoIfoodDataclass(**response.json())
        self.atualizar_dados_internos(instance, dados_ifood)
        return response

    def excluir_registro_ifood(self, instance):
        dados_ifood = self.get_dados_registro_ifood(instance)
        if dados_ifood.fd_ifood_id is None:
            return None

        url = f"catalog/v2.0/merchants/{self.merchant}/products/{dados_ifood.fd_ifood_id}"
        response = self.client.post(url)
        response.raise_for_status()
        instance = self.get_dados_registro_ifood(instance)
        instance.delete()
        return response

    def atualizar_dados_internos(self, instance, dados):
        dados_ifood = self.get_dados_registro_ifood(instance)

    def get_dados_registro_ifood(self, instance):
        instance, _ = ProdutoIfood.objects.get_or_create(fd_produto=instance, defaults={"fd_produto": instance})
        return instance

    def get_id_ifood(self, instance):
        dados_ifood = self.get_dados_registro_ifood(instance)
        return dados_ifood.fd_produto

    def gerar_dados_ifood(self, instance: Produto):
        restricoes_alimentares = []
        if instance.pr_vegano:
            restricoes_alimentares.append("VEGAN")

        if instance.pr_vegetariano:
            restricoes_alimentares.append("VEGETARIAN")

        if instance.pr_organico:
            restricoes_alimentares.append("ORGANIC")

        if instance.pr_sem_gluten:
            restricoes_alimentares.append("GLUTEN_FREE")

        if instance.pr_sem_acucar:
            restricoes_alimentares.append("SUGAR_FREE")

        if instance.pr_zero_lactose:
            restricoes_alimentares.append("LACTOSE_FREE")

        return {
            "name": instance.pr_nome,
            "description": instance.pr_descricao,
            "image": instance.pr_descricao,
            "shifts": [],
            "serving": f"SERVES_{instance.pr_serve_pessoas}" if instance.pr_serve_pessoas else "NOT_APPLICABLE",
            "dietaryRestrictions": restricoes_alimentares,
            "weight": {
                "quantity": instance.pr_quantidade if instance.pr_quantidade else 0,
                "unit": instance.pr_unidade if instance.pr_unidade else "g",
            },
            "optionGroups": [],
        }
