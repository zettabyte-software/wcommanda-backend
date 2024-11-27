import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from django_multitenant.fields import TenantForeignKey

from apps.system.base.models import Base


class Reserva(Base):
    rs_mesa = TenantForeignKey(
        "mesas.Mesa",
        related_name="reservas",
        on_delete=models.PROTECT,
        verbose_name=_("Mesa"),
    )
    rs_cliente = models.CharField(_("cliente"), max_length=80)
    rs_cliente_fidelidade = TenantForeignKey(
        "clientes.Cliente",
        related_name="reservas",
        on_delete=models.PROTECT,
        verbose_name=_("Cliente"),
    )
    rs_data = models.DateField(_("data"))
    rs_hora = models.TimeField(_("hora"))
    rs_quantidade_pessoas = models.PositiveIntegerField(_("pessoas"), default=2)
    rs_observacao = models.TextField(_("observação"), blank=True)
    rs_hora_limite = models.TimeField(_("hora limite de chegada"), null=True)

    class Meta:
        db_table = "reserva"
        ordering = ["-id"]
        verbose_name = _("Reserva")
        verbose_name_plural = _("Reservas")
