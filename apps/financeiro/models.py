from django.db import models
from django.utils.translation import gettext_lazy as _

from django_multitenant.fields import TenantForeignKey

from apps.comandas.models import FormasPagamentoComandaChoices
from apps.system.base.models import Base


class Pagamento(Base):
    pg_venda = TenantForeignKey(
        verbose_name=_("venda"),
        to="vendas.Venda",
        on_delete=models.PROTECT,
        related_name="pagamentos",
    )
    pg_parcela = models.PositiveSmallIntegerField(_("parcela"), default=1)
    pg_valor = models.FloatField(_("parcela"), default=0)
    pg_forma_pagamento = models.PositiveSmallIntegerField(
        _("forma de pagamento"),
        choices=FormasPagamentoComandaChoices.choices,
        null=True,
    )

    class Meta:
        db_table = "pagamento"
        ordering = ["-id"]
        verbose_name = _("Pagamento")
        verbose_name_plural = _("Pagamentos")
