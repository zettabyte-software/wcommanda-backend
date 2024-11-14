from django.conf import settings
from django.core.handlers.wsgi import WSGIRequest

from django_multitenant.utils import set_current_tenant
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from threadlocals.threadlocals import set_current_user

from apps.system.tenants.authentications import JWTAuthentication

from .models import Ambiente


class TenantMiddleware:
    authenticator = JWTAuthentication()

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: WSGIRequest):
        try:
            user, _ = self.authenticator.authenticate(request)
            set_current_user(user)
        except (AuthenticationFailed, TypeError) as exc:
            return self.get_response(request)

        tenant, host = self.get_tenant(request)
        if tenant is None:
            return self.get_response(request)

        request.user = user
        request.tenant = tenant
        request.host = host

        set_current_tenant(tenant)

        return self.get_response(request)

    def get_tenant(self, request: WSGIRequest) -> tuple[Ambiente | None, str]:
        host = self.get_host(request).split(".")[0]
        tenant = Ambiente.objects.filter(mb_subdominio=host).first()
        return tenant, host

    def get_host(self, request: WSGIRequest) -> str:
        if settings.IN_DEVELOPMENT:
            return "zettabyte.wcommanda.com.br"
        return request.headers.get(settings.TENANT_HOST_HEADER, "")
