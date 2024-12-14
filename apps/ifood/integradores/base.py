import logging
import urllib.parse

from django.core.cache import cache

import httpx
import sentry_sdk
from django_multitenant.utils import get_current_tenant

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
