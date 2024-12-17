import dataclasses
import logging

import sentry_sdk
from threadlocals.threadlocals import get_current_user

from apps.filiais.models import Filial
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
    def __init__(self, merchant: str, catalog_id: str):
        super().__init__(merchant)
        self.catalog_id = catalog_id

    def sincronizar_alteracoes_ifood(self, categoria: CategoriaProduto):
        dados = self.gerar_dados_ifood(categoria)
        id_ifood = dados.cd_ifood_id

        if id_ifood is None:
            return self._criar_categoria(dados)

        return self._atualizar_categoria(str(id_ifood), dados)

    def deletar_categoria(self, categoria: CategoriaProduto):
        id_ifood = CategoriaIfood.objects.get(cd_categoria=categoria)
        url = f"catalog/v2.0/merchants/{self.merchant}/categories/{id_ifood}"
        response = self.client.delete(url)
        response.raise_for_status()
        return True

    # rever os 2 métodos abaixo
    def _criar_categoria(self, categoria_ifood: CategoriaIfood):
        url = f"catalog/v2.0/merchants/{self.merchant}/catalogs/{self.catalog_id}/categories"
        response = self.client.post(url, json=categoria_ifood.gerar_dados_ifood())
        response.raise_for_status()
        dados = CategoriaIfoodDataClass(**response.json())
        self._atualizar_cadastro_ifood(categoria_ifood, dados)
        return response

    def _atualizar_categoria(self, id_ifood: str, categoria_ifood: CategoriaIfood):
        url = f"catalog/v2.0/merchants/{self.merchant}/catalogs/{self.catalog_id}/categories/{id_ifood}"
        response = self.client.patch(url, json=categoria_ifood.gerar_dados_ifood(id=True))
        response.raise_for_status()
        return response

    def _atualizar_cadastro_ifood(self, categoria_ifood: CategoriaIfood, dados: CategoriaIfoodDataClass):
        categoria_ifood.cd_ifood_id = dados.id
        categoria_ifood.cd_template = dados.template
        categoria_ifood.cd_index = dados.index
        categoria_ifood.cd_sequence = dados.sequence
        categoria_ifood.save()

    def importar_categorias(self, filial: Filial = None):
        try:
            categorias_ifood = self.get_categorias_ifood()
            for categoria_ifood in categorias_ifood:
                ativo = True if categoria_ifood["status"] == "AVAILABLE" else False
                categoria_wcommanda = CategoriaProduto.objects.create(cg_nome=categoria_ifood["name"], ativo=ativo)

                CategoriaIfood.objects.create(
                    cd_ifood_id=categoria_ifood["id"],
                    cd_categoria=categoria_wcommanda,
                    cd_template=categoria_ifood["template"],
                    cd_index=categoria_ifood["index"],
                    cd_sequence=categoria_ifood["sequence"],
                    owner=get_current_user()  # TODO ver porque o owner não tá pegando sozinho
                    # filial=filial,
                )
        except Exception as e:
            sentry_sdk.capture_exception(e)
            raise e

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
        return 1

    def gerar_dados_ifood(self, categoria: CategoriaProduto):
        print("categoria:", categoria)

        dados_ifood, _ = CategoriaIfood.objects.get_or_create(
            cd_categoria=categoria,
            defaults={
                "cd_categoria": categoria,
            },
        )

        return dados_ifood

        return {
            "id": dados_ifood.cd_ifood_id,
            "name": categoria.cg_nome,
            "status": "AVAILABLE" if categoria.ativo else "UNAVAILABLE",
            "template": dados_ifood.cd_template,
            "sequence": dados_ifood.cd_index,
            "index": dados_ifood.cd_sequence,
        }
