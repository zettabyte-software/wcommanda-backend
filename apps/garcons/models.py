from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from django_multitenant.fields import TenantForeignKey

from apps.system.base.models import Base


class StatusComissaoGarcomChoices(models.IntegerChoices):
    ABERTA = 1, _("Aberto")
    EFETUADA = 2, _("Efetuada")
    ESTORNADA = 3, _("Estornada")
    CANCELADA = 4, _("Cancelada")


class Garcom:
    class Meta:
        db_table = "garcom"
        ordering = ["-id"]
        verbose_name = _("Garçom")
        verbose_name_plural = _("Garçons")


class ComissaoGarcom(Base):

    cg_status = models.PositiveSmallIntegerField(
        _("status"),
        choices=StatusComissaoGarcomChoices.choices,
        default=StatusComissaoGarcomChoices.ABERTA,
    )
    cg_garcom = TenantForeignKey(
        verbose_name=_("garçom"),
        to=settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="comissoes",
    )
    cg_comanda = TenantForeignKey(verbose_name=_("comanda"), to="comandas.Comanda", on_delete=models.PROTECT)
    cg_valor_total_comanda = models.FloatField(_("valor da comanda"), default=0)
    cg_valor = models.FloatField(_("valor"), default=0)
    cg_percentual = models.FloatField(_("percentual da comissão"), default=0)

    class Meta:
        db_table = "comissao_garcom"
        ordering = ["-id"]
        verbose_name = _("Comissão do Garçom")
        verbose_name_plural = _("Comissões do Garçons")
