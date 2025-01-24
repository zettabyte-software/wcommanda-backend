from django.conf import settings
from django.contrib.auth.hashers import make_password

from django_multitenant.utils import set_current_tenant

from apps.system.core.records import DefaultRecordsManger
from apps.system.tenants.models import Ambiente
from apps.users.models import Usuario
from lib.cloudflare.dns import create_dns_record


class TenantManager:
    def criar_tenant(self, dados_ambient, dados_usuario):
        self.criar_ambiente(dados_ambient["mb_nome"], dados_ambient["mb_subdominio"])
        self.criar_usuario_root(
            dados_usuario["first_name"],
            dados_usuario["last_name"],
            dados_usuario["email"],
            dados_usuario["password"],
        )
        self.popular_registros_padroes()

    def criar_ambiente(self, nome, subdominio):
        ambiente = Ambiente.objects.create(mb_subdominio=subdominio, mb_nome=nome)
        set_current_tenant(ambiente)
        if settings.IN_PRODUCTION:
            create_dns_record(ambiente.mb_subdominio)

    def criar_usuario_root(self, nome: str, sobrenome: str, email: str, senha: str):
        usuario = Usuario()
        usuario.first_name = nome
        usuario.last_name = sobrenome
        usuario.email = email
        usuario.password = make_password(senha)
        usuario.save()

    def popular_registros_padroes(self):
        manager = DefaultRecordsManger()
        manager.populate()
