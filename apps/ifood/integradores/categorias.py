import dataclasses
import logging

from apps.ifood.models import CategoriaIfood
from apps.produtos.models import CategoriaProduto

from .base import BaseIntegradorIfood

logger = logging.getLogger(__name__)

LIMITE_REGISTROS = 100


@dataclasses.dataclass
class CategoriaIfoodDataClass:
    id: str
    name: str
    status: str
    sequence: int
    index: int
    template: str


class IntegradorCategoriasIfood(BaseIntegradorIfood):
    def __init__(self, client_id: str, client_secret: str, merchant: str, catalog_id: str):
        super().__init__(client_id, client_secret, merchant)
        self.catalog_id = catalog_id

    def importar_categorias(self):
        categorias_ifood = self.get_categorias_ifood()
        for categoria_ifood in categorias_ifood:
            ativo = True if categoria_ifood["status"] == "AVAILABLE" else False
            categoria_wcommanda = CategoriaProduto.objects.create(
                cg_nome=categoria_ifood["name"],
                cg_descricao="Categoria integrada via iFood",
                ativo=ativo
            )

            CategoriaIfood.objects.create(
                cd_ifood_id=categoria_ifood["id"],
                cd_categoria=categoria_wcommanda,
                cd_template_pizza=categoria_ifood["template"],
                cd_index=categoria_ifood["index"],
                cd_sequence=categoria_ifood["sequence"],
            )

    def get_categorias_ifood(self):
        page = 1
        total_paginas = self.get_total_paginas()
        produtos = []

        while page <= total_paginas:
            produtos_pagina = self._get_categorias_ifood(page)
            produtos.extend(produtos_pagina)
            page += 1

        return produtos

    def _get_categorias_ifood(self, page):
        response = self.client.get(
            f"catalog/v2.0/merchants/{self.merchant}/catalogs/{self.catalog_id}/categories?limit={LIMITE_REGISTROS}&page={page}&includeItems=false"
        )
        response.raise_for_status()
        return response.json()

    def get_total_paginas(self):
        response = self.client.get(f"catalog/v2.0/merchants/{self.merchant}/catalogs/{self.catalog_id}/categories?limit={LIMITE_REGISTROS}&includeItems=false")
        dados = response.json()
        return dados["count"] // LIMITE_REGISTROS + 1

    def gerar_dados_categoria_ifood(self, categoria: CategoriaProduto):
        dados_ifood = CategoriaIfood.objects.get_or_create(
            cd_categoria=categoria,
            defaults={
                "cd_categoria": categoria,
            },
        )

        return {
            "name": categoria.cg_nome,
            "status": "AVAILABLE" if categoria.ativo else "UNAVAILABLE",
            "template": "DEFAULT",
            "sequence": 1,
            "index": 1,
        }
