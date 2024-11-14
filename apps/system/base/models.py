import json

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.forms.models import model_to_dict
from django.utils.translation import gettext_lazy as _

from auditlog.models import AuditlogHistoryField, LogEntry
from django_multitenant.fields import TenantForeignKey
from django_multitenant.models import TenantModel
from threadlocals.threadlocals import get_current_user


class Base(TenantModel):
    tenant_id = "ambiente_id"

    ativo = models.BooleanField(
        _("ativo"),
        default=True,
    )

    codigo = models.PositiveBigIntegerField(
        _("código"),
        editable=False,
        default=1,
    )

    data_criacao = models.DateField(_("data de criação"), auto_now_add=True)
    hora_criacao = models.TimeField(_("hora de criação"), auto_now_add=True)
    data_ultima_alteracao = models.DateField(_("data da última alteração"), auto_now=True)
    hora_ultima_alteracao = models.TimeField(_("hora da última alteração"), auto_now=True)

    filial = TenantForeignKey(
        "filiais.Filial",
        verbose_name=_("filial"),
        on_delete=models.PROTECT,
        null=True,
    )

    owner = TenantForeignKey(
        verbose_name=_("owner"),
        to=settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        null=True,
    )

    ambiente = models.ForeignKey(
        "tenants.Ambiente",
        verbose_name=_("tenant"),
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    history = AuditlogHistoryField()

    @property
    def json(self):
        data = model_to_dict(self)
        return json.dumps(data, default=str)

    @property
    def historico_alteracoes(self):
        content_type = ContentType.objects.get_for_model(self)
        return LogEntry.objects.filter(content_type=content_type, object_id=self.pk).order_by("-timestamp")

    all_objects = models.Manager()

    def save(self, *args, **kwargs):
        if not hasattr(self, "owner"):
            self.owner = get_current_user()

        last = self.__class__.objects.all().order_by("codigo").last()
        if last:
            self.codigo = last.codigo + 1
        else:
            self.codigo = 1

        return super().save(*args, **kwargs)

    class Meta:
        abstract = True


class EstadosChoices(models.TextChoices):
    EM_BRANCO = 0, "Em branco"
    RONDONIA = 1, "Rondônia"
    ACRE = 2, "Acre"
    AMAZONAS = 3, "Amazonas"
    RORAIMA = 4, "Roraima"
    PARA = 5, "Pará"
    AMAPA = 6, "Amapá"
    TOCANTINS = 7, "Tocantins"
    MARANHAO = 8, "Maranhão"
    PIAUI = 9, "Piauí"
    CEARA = 10, "Ceará"
    RIO_GRANDE_DO_NORTE = 11, "Rio Grande do Norte"
    PARAIBA = 12, "Paraíba"
    PERNAMBUCO = 13, "Pernambuco"
    ALAGOAS = 14, "Alagoas"
    SERGIPE = 15, "Sergipe"
    BAHIA = 16, "Bahia"
    MINAS_GERAIS = 17, "Minas Gerais"
    ESPIRITO_SANTO = 18, "Espírito Santo"
    RIO_DE_JANEIRO = 19, "Rio de Janeiro"
    SAO_PAULO = 20, "São Paulo"
    PARANA = 21, "Paraná"
    SANTA_CATARINA = 22, "Santa Catarina"
    RIO_GRANDE_DO_SUL = 23, "Rio Grande do Sul"
    MATO_GROSSO_DO_SUL = 24, "Mato Grosso do Sul"
    MATO_GROSSO = 25, "Mato Grosso"
    GOIAS = 26, "Goiás"
    DISTRITO_FEDERAL = 27, "Distrito Federal"
    EXTERIOR = 28, "Exterior"
