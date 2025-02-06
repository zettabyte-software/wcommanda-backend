from django.conf import settings
from django.contrib.auth.hashers import make_password

from django_multitenant.utils import set_current_tenant

from apps.system.assinaturas.models import Assinatura
from apps.system.core.records import DefaultRecordsManger
from apps.users.models import Usuario
from lib.cloudflare.dns import create_dns_record


class InicializadorAssinatura:
    def criar_assinatura(self, dados_ambient, dados_usuario):
        self._criar_assinatura(dados_ambient["mb_nome"], dados_ambient["mb_subdominio"])
        self.criar_usuario_root(
            dados_usuario["first_name"],
            dados_usuario["last_name"],
            dados_usuario["email"],
            dados_usuario["password"],
        )
        self.popular_registros_padroes()

    def _criar_assinatura(self, nome: str, subdominio: str):
        raise Exception

        # assinatura = Assinatura.objects.create(
        #     ss_subdominio=subdominio,
        #     ss_nome=nome,
        #     ss_cloudflare_id="dev-id",
        #     ss_status=StatusChoices.ULTRA,
        # )
        # plano = Plano.objects.create(
        #     pl_nome="Dev",
        #     pl_tier=TierChoices.TIER_4,
        #     pl_numero_usuarios=100,
        #     pl_limite_integracoes_ifood=99999,
        #     pl_valor_mensalidade=0,
        #     pl_observacao="",
        #     assinatura=assinatura,
        # )

        # set_current_tenant(ambiente)
        # if settings.IN_PRODUCTION:
        #     create_dns_record(ambiente.mb_subdominio)

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
