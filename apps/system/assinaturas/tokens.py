from django.conf import settings
from django.utils.translation import gettext_lazy as _

from rest_framework_simplejwt.backends import TokenBackend
from rest_framework_simplejwt.exceptions import TokenBackendError, TokenError
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import AccessToken as SimpleJWTAccessToken
from rest_framework_simplejwt.utils import aware_utcnow
from threadlocals.threadlocals import get_current_request


class AccessToken(SimpleJWTAccessToken):
    def __init__(self, token=None, verify=True, request=None) -> None:
        if self.token_type is None or self.lifetime is None:
            raise TokenError(_("Cannot create token with no type or lifetime"))

        self.token = token
        self.current_time = aware_utcnow()
        self.audience = self.get_host()

        if token is not None:
            token_backend = self.get_token_backend()

            try:
                self.payload = token_backend.decode(token, verify=verify)
            except TokenBackendError as e:
                raise TokenError(_("Token is invalid or expired")) from e

            if verify:
                self.verify()
        else:
            self.payload = {api_settings.TOKEN_TYPE_CLAIM: self.token_type}

            self.set_exp(from_time=self.current_time, lifetime=self.lifetime)
            self.set_iat(at_time=self.current_time)

            self.set_jti()

    def get_token_backend(self) -> TokenBackend:
        return TokenBackend(
            api_settings.ALGORITHM,
            api_settings.SIGNING_KEY,
            api_settings.VERIFYING_KEY,
            self.audience,
            api_settings.ISSUER,
            api_settings.JWK_URL,
            api_settings.LEEWAY,
            api_settings.JSON_ENCODER,
        )

    def get_host(self) -> str:
        if settings.IN_DEVELOPMENT:
            return "zettabyte.wcommanda.com.br"
        request = get_current_request()
        return request.headers.get(settings.TENANT_HOST_HEADER)
