from django.conf import settings
from django.contrib.auth.hashers import make_password

from django_multitenant.utils import set_current_tenant

from apps.system.assinaturas.models import Assinatura, Plano, StatusChoices, TierChoices
from apps.system.core.records import DefaultRecordsManger
from apps.users.models import Usuario
from lib.cloudflare.dns import criar_subdominio


# TODO criar testes para criação de assinatura
class InicializadorAssinatura:
    def criar_assinatura(self, dados_ambiente: dict, dados_usuario: dict, tier: TierChoices):
        self._criar_assinatura(dados_ambiente["mb_nome"], dados_ambiente["mb_subdominio"], tier)
        self.criar_usuario_root(
            dados_usuario["first_name"],
            dados_usuario["last_name"],
            dados_usuario["email"],
            dados_usuario["password"],
        )
        self.popular_registros_padroes()

    def _criar_assinatura(self, nome: str, subdominio: str, tier: TierChoices):
        assinatura = Assinatura.objects.create(
            ss_subdominio=subdominio,
            ss_nome=nome,
            ss_cloudflare_id="dev-id",
            ss_status=StatusChoices.ULTRA,
        )

        Plano.criar_plano(tier)

        set_current_tenant(assinatura)

        if settings.IN_PRODUCTION:
            criar_subdominio(assinatura.ss_subdominio)

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
