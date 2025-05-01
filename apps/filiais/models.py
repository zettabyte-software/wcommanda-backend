import uuid

from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from django.utils.translation import gettext_lazy as _

from auditlog.registry import auditlog
from django_multitenant.fields import TenantForeignKey
from django_multitenant.utils import get_current_tenant

from apps.system.base.models import Base, EstadosChoices
from lib.back_blaze.bucket import BackBlazeB2Handler

DEFAULT_BUCKET_BRANCH_LOGO_PATH = "%s/filiais/%s/imgs/%s"
"""Caminho padrão para a imagem dentro do bucket: \n
[id_tenant]/filiais/[id_filial]/imgs/[nome_arquivo]
"""


class Filial(Base):
    filial = None

    # informações básicas
    fl_nome = models.CharField(_("nome"), max_length=120)

    fl_cep = models.CharField(_("cep"), max_length=8, blank=True, default="")
    fl_estado = models.PositiveSmallIntegerField(
        _("estado"),
        choices=EstadosChoices.choices,
        default=EstadosChoices.EM_BRANCO,
    )
    fl_cidade = models.CharField(_("cidade"), max_length=50, blank=True, default="")
    fl_bairro = models.CharField(_("bairro"), max_length=40, blank=True, default="")
    fl_rua = models.CharField(_("rua"), max_length=30, blank=True, default="")
    fl_numero = models.CharField(_("número"), max_length=8, blank=True, default="")
    fl_complemento = models.CharField(_("complemento"), max_length=100, blank=True, default="")

    # contato
    fl_celular = models.CharField(_("celular"), max_length=11, blank=True)
    fl_telefone = models.CharField(_("telefone"), max_length=10, blank=True)
    fl_email = models.EmailField(_("email"), blank=True)

    # funcionamento
    fl_hora_inicio_funcionamento_domingo = models.TimeField(_("horário de início no domingo"), null=True)
    fl_hora_fim_funcionamento_domingo = models.TimeField(_("horário de encerramento no domingo"), null=True)

    fl_hora_inicio_funcionamento_segunda = models.TimeField(_("horário de início na segunda-feira"), null=True)
    fl_hora_fim_funcionamento_segunda = models.TimeField(_("horário de encerramento na segunda-feira"), null=True)

    fl_hora_inicio_funcionamento_terca = models.TimeField(_("horário de início na terca-feira"), null=True)
    fl_hora_fim_funcionamento_terca = models.TimeField(_("horário de encerramento na terca-feira"), null=True)

    fl_hora_inicio_funcionamento_quarta = models.TimeField(_("horário de início na quarta-feira"), null=True)
    fl_hora_fim_funcionamento_quarta = models.TimeField(_("horário de encerramento na quarta-feira"), null=True)

    fl_hora_inicio_funcionamento_quinta = models.TimeField(_("horário de início na quinta-feira"), null=True)
    fl_hora_fim_funcionamento_quinta = models.TimeField(_("horário de encerramento na quinta-feira"), null=True)

    fl_hora_inicio_funcionamento_sexta = models.TimeField(_("horário de início na sexta-feira"), null=True)
    fl_hora_fim_funcionamento_sexta = models.TimeField(_("horário de encerramento na sexta-feira"), null=True)

    fl_hora_inicio_funcionamento_sabado = models.TimeField(_("horário de início no sabado"), null=True)
    fl_hora_fim_funcionamento_sabado = models.TimeField(_("horário de encerramento no sabado"), null=True)

    # ifood
    fl_client_secret_ifood = models.CharField(_("clientId do iFood"), max_length=300, blank=True, default="")
    fl_client_id_ifood = models.UUIDField(_("clientSecret do iFood"), null=True, default=None)

    fl_merchat_id_ifood = models.UUIDField(_("id do merchant do iFood"), null=True, default=None)
    fl_catalog_id = models.UUIDField(_("id do catálogo digital do iFood"), null=True, default=None)
    fl_catalog_group_id = models.UUIDField(_("id do grupo do catálogo do iFood"), null=True, default=None)

    # TODO remover
    fl_url_logo = models.URLField(_("url amigável da foto"), blank=True, default="")
    fl_path_logo = models.CharField(_("caminho da logo no bucket"), max_length=120, blank=True, default="")
    fl_id_back_blaze = models.CharField(_("id backblaze do upload"), max_length=40, blank=True, default="")

    # sobreescrevendo por causa do related_name
    owner = TenantForeignKey(
        verbose_name=_("owner"),
        to=settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        null=True,
        related_name="filiais",
    )

    # TODO remover
    @classmethod
    def upload(cls, filial: "Filial", arquivo: InMemoryUploadedFile, metadata=None):
        if metadata is None:
            metadata = {}

        handler = BackBlazeB2Handler()
        assinatura = get_current_tenant()
        extencao = arquivo.name.split(".")[-1]
        nome_aleatorio_imagem = f'{uuid.uuid4()}.{extencao}'

        path = DEFAULT_BUCKET_BRANCH_LOGO_PATH % (
            assinatura.ss_codigo_licenca,  # type: ignore
            filial.pk,
            nome_aleatorio_imagem,
        )

        file_version = handler.upload(arquivo.read(), path, metadata)

        filial.fl_url_logo = f"https://f005.backblazeb2.com/file/wcommanda/{path}"
        filial.fl_path_logo = path
        filial.fl_id_back_blaze = file_version.id_

        filial.save()

    class Meta:
        db_table = "filial"
        ordering = ["-id"]
        verbose_name = _("Filial")
        verbose_name_plural = _("Filiais")


auditlog.register(
    Filial,
    exclude_fields=[
        "data_ultima_alteracao",
        "hora_ultima_alteracao",
    ],
)
