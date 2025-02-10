import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from auditlog.registry import auditlog
from django_multitenant.fields import TenantForeignKey

from apps.system.base.models import Base


# TODO fazer uma background task para enviar um SMS lembrando a pessoa da reserva
class Reserva(Base):
    rs_codigo = models.UUIDField(_("código da reserva"), default=uuid.uuid4)
    rs_mesa = TenantForeignKey(
        "mesas.Mesa",
        related_name="reservas",
        on_delete=models.PROTECT,
        verbose_name=_("Mesa"),
    )
    rs_cliente = models.CharField(_("cliente"), max_length=80)
    rs_celular_cliente = models.CharField(_("cliente"), max_length=11, blank=True, default="")
    rs_cliente_fidelidade = TenantForeignKey(
        "clientes.Cliente",
        verbose_name=_("cliente fidelidade"),
        related_name="reservas",
        on_delete=models.PROTECT,
        null=True,
    )
    rs_data = models.DateField(_("data"))
    rs_hora = models.TimeField(_("hora"))
    rs_quantidade_pessoas = models.PositiveIntegerField(_("pessoas"), default=2)
    rs_observacao = models.TextField(_("observação"), blank=True)
    rs_hora_limite = models.TimeField(_("hora limite de chegada"), null=True)
    # rs_minutos_envio_sms = models.TimeField(_(""), null=True)  # enviar um sms x minutos antes lembrando a reserva

    class Meta:
        db_table = "reserva"
        ordering = ["-id"]
        verbose_name = _("Reserva")
        verbose_name_plural = _("Reservas")


auditlog.register(
    Reserva,
    exclude_fields=[
        "data_ultima_alteracao",
        "hora_ultima_alteracao",
    ],
)
