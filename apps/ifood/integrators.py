import logging
import urllib.parse

from django.core.cache import cache
from django.db import transaction

import httpx
import sentry_sdk
from django_multitenant.utils import get_current_tenant
from threadlocals.threadlocals import get_current_request, get_current_user

from apps.produtos.models import Produto
from apps.produtos.services import gerar_codigo_cardapio
from utils.jwt import decode_jwt

from .dataclasses import EventoIfood
from .models import PedidoIfood, ProdutoIfood

_BASE_URL_API_IFOOD = "https://merchant-api.ifood.com.br"
_BASE_HEADERS_IFOOD = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "User-Agent": "wCommanda (wcommanda.com.br) - v2.0.0",
}

logger = logging.getLogger(__name__)


class BaseIntegradorIfood:
    def __init__(self, client_id: str, client_secret: str, merchant: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.merchant = "85330304-7ee6-4182-b40d-6c65cca35a65"

        self.client = httpx.Client(
            base_url=_BASE_URL_API_IFOOD,
            headers=_BASE_HEADERS_IFOOD,
        )

        token = self.get_token_ifood()

        self.client.headers["Authorization"] = f"Bearer {token}"

    def get_token_ifood(self) -> str | None:
        logger.info("Obtendo token do iFood do tenant %s", get_current_tenant())

        token_cache_key = f"token_ifood_{self.client_id}"
        token = cache.get(token_cache_key, None)

        if token is None:
            logger.info("Token não encontrado no cache, realizando login no iFood")
            token, expiracao = self.login_ifood()
            cache.set(token_cache_key, token, timeout=expiracao)

        return token

    def login_ifood(self) -> tuple[str, int]:
        logger.info("Iniciando o login no iFood")
        data = {
            "grantType": "client_credentials",
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
            "authorizationCode": "",
            "authorizationCodeVerifier": "",
            "refreshToken": "",
        }

        logger.debug(urllib.parse.urlencode(data))
        try:
            response = httpx.post(
                "https://merchant-api.ifood.com.br/authentication/v1.0/oauth/token",
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                data=urllib.parse.urlencode(data),
            )

            logger.info(response.text)
            response.raise_for_status()
            dados = response.json()
            return dados["accessToken"], dados["expiresIn"]
        except (httpx.HTTPStatusError, httpx.DecodingError) as e:
            logger.error("Erro ao realizar login no iFood: %s", e)
            sentry_sdk.capture_exception(e)
            raise e


class IntegradorPedidosIfood(BaseIntegradorIfood):
    def criar_pedido_via_webhook(self, evento_ifood: EventoIfood) -> PedidoIfood | None:
        dados_pedido = self.get_dados_pedido(evento_ifood.orderId)
        if dados_pedido is None:
            return

        pedido = PedidoIfood.objects.create(
            id_ifood=dados_pedido["id"],
            status=dados_pedido["status"],
            valor_total=dados_pedido["total"],
            cliente=dados_pedido["customer"]["name"],
            endereco_entrega=dados_pedido["deliveryAddress"]["formattedAddress"],
            pedido=dados_pedido,
        )

        return pedido

    def get_dados_pedido(self, id_ifood: str) -> dict | None:
        try:
            response = self.client.get(f"merchants/{self.merchant}/orders/{id_ifood}")
            response.raise_for_status()
            return response.json()
        except (httpx.HTTPStatusError, httpx.DecodingError) as e:
            logger.error("Erro ao realizar login no iFood: %s", e)
            sentry_sdk.capture_exception(e)
            return None


class IntegradorProdutoIfood(BaseIntegradorIfood):
    def integrar_produto(self, produto: Produto):
        dados = self.gerar_dados_produto(produto)
        if produto.pr_id_ifood is None:
            response = self.client.post(f"merchants/{self.merchant}/product/")
        else:
            response = self.client.post(f"merchants/{self.merchant}/product/{produto.pr_id_ifood}")

        return response

    def gerar_dados_produto(self, produto: Produto):
        return {
            "name": produto.pr_nome,
            "description": produto.pr_descricao,
            "image": produto.pr_descricao,
            "shifts": [],
            "serving": "NOT_APPLICABLE",
            "dietaryRestrictions": [],
            "weight": {"quantity": 0, "unit": "g"},
            "optionGroups": [],
        }


class ImportarProdutosIfood(BaseIntegradorIfood):
    LIMIT = 100
    endpoint = "catalog/v2.0/merchants/%s/products?limit=%i&page=%i"

    def importar_produtos(self):
        produtos_ifood = self.get_produtos_ifood()
        for produto in produtos_ifood:
            p = Produto.objects.create(
                pr_nome=produto["name"],
                pr_descricao=produto.get("description", "Produto integrado via iFood"),
                pr_codigo_cardapio=gerar_codigo_cardapio()
            )

            # ProdutoIfood.objects.create(
            #     produto["id"],
            #     fd_produto=p,
            # )

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
        response = self.client.get(f"catalog/v2.0/merchants/{self.merchant}/products?limit={self.LIMIT}&page={page}")
        response.raise_for_status()
        return response.json()["elements"]

    def get_total_paginas_produtos(self):
        response = self.client.get(f"catalog/v2.0/merchants/{self.merchant}/products?limit={self.LIMIT}&page=1")
        dados = response.json()
        return dados["count"] // self.LIMIT + 1
