import hashlib
import hmac
import logging

from django.core.exceptions import ImproperlyConfigured

from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed

from apps.system.conf.models import Configuracao

logger = logging.getLogger(__name__)


class IFoodWebhookAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        signature_header = request.META.get("HTTP_X_IFOOD_SIGNATURE")
        if not signature_header:
            return None

        body = request.body

        try:
            raise NotImplementedError("Removido")
            client_secret = None
        except AttributeError as e:
            raise ImproperlyConfigured("IFOOD_CLIENT_SECRET not configured in settings") from e

        calculated_signature = self._calcular_assinatura(body, client_secret)

        if not hmac.compare_digest(calculated_signature, signature_header):
            raise AuthenticationFailed("Invalid signature")

        return (None, None)

    def _calcular_assinatura(self, message: str, secret: str):
        if isinstance(secret, str):
            secret = secret.encode("utf-8")

        if isinstance(message, str):
            message = message.encode("utf-8")

        digest = hmac.new(secret, message, hashlib.sha256).hexdigest()
        return digest
