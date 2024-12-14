from apps.produtos.models import Produto
from apps.produtos.services import gerar_codigo_cardapio

from .base import BaseIntegradorIfood

# https://merchant-api.ifood.com.br/catalog/v2.0/merchants/6b487a27-c4fc-4f26-b05e-3967c2331882/inventory
d = {"productId": "ec16fb62-7bdd-43e4-940c-10b5a2845f13", "amount": 10}

LIMITE_REGISTROS = 100


class ImportadorProdutosIfoodMixin(BaseIntegradorIfood):
    def importar_produtos(self):
        produtos_ifood = self.get_produtos_ifood()
        for produto_ifood in produtos_ifood:
            produto_wcommanda = Produto.objects.create(
                pr_nome=produto_ifood["name"],
                pr_descricao=produto_ifood.get("description", "Produto integrado via iFood"),
                pr_codigo_cardapio=gerar_codigo_cardapio(),
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
        pass
