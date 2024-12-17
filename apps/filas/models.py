from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.system.base.models import Base


class Fila(Base):
    ff_posicao = models.PositiveSmallIntegerField(_("posição"), default=1)
    ff_cliente = models.CharField(_("cliente"), max_length=40)
    ff_telefone = models.CharField(_("cliente"), max_length=11)
    ff_observacao = models.CharField(_("cliente"), max_length=60)

    class Meta:
        db_table = "fila"
        ordering = ["-id"]
        verbose_name = _("Fila")
        verbose_name_plural = _("Filas")
