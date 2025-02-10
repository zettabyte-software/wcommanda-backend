from django.db import models
from django.utils.translation import gettext_lazy as _

from auditlog.registry import auditlog

from apps.system.base.models import Base


class Mesa(Base):
    ms_codigo = models.PositiveSmallIntegerField(_("código"))
    ms_quantidade_lugares = models.PositiveSmallIntegerField(_("quantidade de lugares"))
    ms_ocupada = models.BooleanField(_("ocupada"), default=False)
    ms_observacao = models.CharField(_("observacao"), max_length=100, blank=True)

    class Meta:
        db_table = "mesa"
        ordering = ["-id"]
        verbose_name = _("Mesa")
        verbose_name_plural = _("Mesas")


auditlog.register(
    Mesa,
    exclude_fields=[
        "data_ultima_alteracao",
        "hora_ultima_alteracao",
    ],
)
