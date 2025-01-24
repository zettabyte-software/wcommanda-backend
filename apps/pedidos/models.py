import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from django_multitenant.fields import TenantForeignKey

from apps.system.base.models import Base, EstadosChoices


class Pedido(Base):
    dd_codigo = models.UUIDField(_("código"), default=uuid.uuid4)

    dd_cliente = models.CharField(_("cliente"), max_length=30, blank=True)
    dd_cliente_fidelidade = TenantForeignKey(verbose_name=_("cliente fidelidade"), to="clientes.Cliente", on_delete=models.PROTECT, null=True)

    dd_entrega = models.BooleanField(_("tem entrega"))

    dd_cep = models.CharField(_("cep"), max_length=8, blank=True, default="")
    dd_estado = models.PositiveSmallIntegerField(_("estado"), choices=EstadosChoices.choices, default=EstadosChoices.EM_BRANCO)
    dd_cidade = models.CharField(_("cidade"), max_length=50, blank=True, default="")
    dd_bairro = models.CharField(_("bairro"), max_length=40, blank=True, default="")
    dd_rua = models.CharField(_("rua"), max_length=30, blank=True, default="")
    dd_numero = models.CharField(_("número"), max_length=8, blank=True, default="")
    dd_complemento = models.CharField(_("complemento"), max_length=100, blank=True, default="")

    class Meta:
        db_table = "pedido"
        ordering = ["-id"]
        verbose_name = _("Pedido")
        verbose_name_plural = _("Pedidos")


class PedidoItem(Base):
    dt_pedido = TenantForeignKey(verbose_name=_("pedido"), to="pedidos.Pedido", on_delete=models.CASCADE)
    dt_produto = TenantForeignKey(verbose_name=_("pedido"), to="produtos.Produto", on_delete=models.CASCADE)
    dt_quantidade = models.PositiveSmallIntegerField(_("quantidade"))
    dt_observacao = models.CharField(_("observação"), max_length=100)

    class Meta:
        db_table = "pedido_item"
        ordering = ["-id"]
        verbose_name = _("Item do Pedido")
        verbose_name_plural = _("Itens dos Pedidos")
