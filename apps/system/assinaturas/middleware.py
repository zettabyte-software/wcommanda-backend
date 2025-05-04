import logging

from django.conf import settings
from django.core.handlers.wsgi import WSGIRequest

from django_multitenant.utils import set_current_tenant
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from threadlocals.threadlocals import set_current_user, set_request_variable

from apps.filiais.models import Filial
from apps.system.core.authentications import JWTAuthentication
from utils.jwt import decode_jwt

from .models import Assinatura

logger = logging.getLogger(__name__)


class AssinaturaMiddleware:
    authenticator = JWTAuthentication()

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: WSGIRequest):
        token = self.get_token(request)

        if token is None:
            return self.get_response(request)

        tenant, subdomain = self.get_tenant(request)

        if tenant is None:
            return self.get_response(request)

        request.tenant = tenant
        request.host = subdomain

        filial = self.get_filial(request)
        host = self.get_host(request)

        set_current_tenant(tenant)

        set_request_variable("host", host)
        set_request_variable("subdomain", subdomain)
        set_request_variable("filial", filial)

        try:
            user, _ = self.authenticator.authenticate(request)  # type: ignore
            set_current_user(user)
        except (AuthenticationFailed, TypeError):
            return self.get_response(request)

        request.user = user

        token = request.headers.get("Authorization")

        set_request_variable("token", token.split(" ")[1] if token else None)

        return self.get_response(request)

    def get_tenant(self, request: WSGIRequest) -> tuple[Assinatura | None, str]:
        host = self.get_host(request).split(".")[0]
        tenant = Assinatura.objects.filter(ss_subdominio=host).first()
        return tenant, host

    def get_host(self, request: WSGIRequest) -> str:
        return request.headers.get(settings.TENANT_HOST_HEADER, "")

    def get_token(self, request: WSGIRequest) -> str:
        return request.headers.get("Authorization", None)

    def get_filial(self, request: WSGIRequest) -> None | Filial:
        token = request.headers.get("Authorization", None)
        if token is None:
            return None

        host = self.get_host(request)
        token = token.split(" ")[1]
        id_filial = decode_jwt(token, host).get("branch", 0)

        filial = Filial.objects.filter(pk=id_filial).first()

        return filial
