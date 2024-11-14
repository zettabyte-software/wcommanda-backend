import logging

from django.core.cache import cache

import httpx
import sentry_sdk
from django_multitenant.utils import get_current_tenant
from threadlocals.threadlocals import get_current_request, get_current_user

from apps.produtos.models import Produto
from utils.jwt import decode_jwt

from .dataclasses import EventoIfood
from .models import PedidoIfood

_BASE_URL_API_IFOOD = "https://merchant-api.ifood.com.br"
_BASE_HEADERS_IFOOD = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "User-Agent": "Wcommanda (wcommanda.com.br) - v2.0.0",
}

logger = logging.getLogger(__name__)


class BaseIntegradorIfood:
    def __init__(self, client_id: str, client_secret: str, merchant: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.merchant = merchant

        token = self.get_token_ifood()
        self.client = httpx.Client(
            base_url=_BASE_URL_API_IFOOD,
            headers={
                **_BASE_HEADERS_IFOOD,
                "Authorization": f"Bearer {token}",
            },
        )

    def get_token_ifood(self) -> str | None:
        logger.info(
            "Obtendo token do iFood do client_id: %s do tenant: %s",
            self.client_id,
            get_current_tenant(),
        )
        token_cache_key = f"token_ifood_{self.client_id}"
        token = cache.get(token_cache_key, None)

        if token is None:
            logger.info("Token não encontrado no cache, realizando login no iFood")
            token, expiracao = self.login_ifood()
            if token is None:
                return None
            cache.set(token_cache_key, token, timeout=expiracao)

        return token

    def login_ifood(self) -> tuple[str, int] | tuple[None, None]:
        logger.info("Realizando login no iFood")
        data = {
            "grantType": "client_credentials",
            "clientId": self.client_id,
            "clientSecret": self.client_secret,
            "authorizationCode": "",
            "authorizationCodeVerifier": "",
            "refreshToken": "",
        }

        try:
            response = httpx.post(
                "authentication/v1.0/oauth/token",
                headers={
                    **_BASE_HEADERS_IFOOD,
                    "Content-Type": "application/x-www-form-urlencoded",
                },
                data=data,
            )
            response.raise_for_status()
            dados = response.json()
            return dados["accessToken"], dados["expiresIn"]
        except (httpx.HTTPStatusError, httpx.DecodingError) as e:
            logger.error("Erro ao realizar login no iFood: %s", e)
            sentry_sdk.capture_exception(e)
            return None, None


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
            response = self.client.post(
                f"merchants/{self.merchant}/product/{produto.pr_id_ifood}"
            )

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
