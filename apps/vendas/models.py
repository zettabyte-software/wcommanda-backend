from django.db import models
from django.utils.translation import gettext_lazy as _

from django_multitenant.fields import TenantForeignKey

from apps.system.base.models import Base


class Venda(Base):
    vn_comanda = TenantForeignKey(
        verbose_name=_("comanda"),
        to="comandas.Comanda",
        on_delete=models.PROTECT,
        related_name="vendas",
    )

    vn_cliente = models.CharField(_("cliente"), max_length=30)
    vn_cliente_fidelidade = TenantForeignKey(
        verbose_name=_("cliente fidelidade"),
        to="clientes.Cliente",
        on_delete=models.PROTECT,
        null=True,
    )

    vn_valor_total = models.FloatField(_("valor total"), default=0)

    class Meta:
        db_table = "venda"
        ordering = ["-id"]
        verbose_name = _("Venda")
        verbose_name_plural = _("Vendas")


class VendaItem(Base):
    vd_venda = TenantForeignKey(
        verbose_name=_("venda"),
        to="vendas.Venda",
        on_delete=models.CASCADE,
        related_name="itens",
    )

    vd_produto = TenantForeignKey(
        verbose_name=_("venda"),
        to="produtos.Produto",
        on_delete=models.CASCADE,
        related_name="venda_itens",
    )

    vd_quantidade = models.FloatField(_("quantidade"), default=0)

    vd_preco_unitario_produto = models.FloatField(_("preço unitário"), default=0)

    vd_valor_total = models.FloatField(_("valor total"), default=0)

    class Meta:
        db_table = "venda_item"
        ordering = ["-id"]
        verbose_name = _("Item da Venda")
        verbose_name_plural = _("Itens da Venda")
