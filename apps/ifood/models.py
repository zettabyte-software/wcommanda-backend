from django.db import models
from django.utils.translation import gettext_lazy as _

from django_multitenant.fields import TenantForeignKey

from apps.system.base.models import Base


class TipoEventoIfood(models.IntegerChoices):
    ORDER_STATUS = 1, "ORDER_STATUS"
    CANCELLATION_REQUEST = 2, "CANCELLATION_REQUEST"
    HANDSHAKE_PLATFORM = 3, "HANDSHAKE_PLATFORM"
    ORDER_TAKEOUT = 4, "ORDER_TAKEOUT"
    DELIVERY = 5, "DELIVERY"
    DELIVERY_ADDRESS = 6, "DELIVERY_ADDRESS"
    DELIVERY_GROUP = 7, "DELIVERY_GROUP"
    DELIVERY_ONDEMAND = 8, "DELIVERY_ONDEMAND"
    DELIVERY_COMPLEMENT = 9, "DELIVERY_COMPLEMENT"
    ORDER_MODIFIER = 10, "ORDER_MODIFIER"
    OUTROS = 99, "OUTROS"


class ProdutoIfood:
    fd_ifood_id = models.UUIDField(_("id do produto no iFood"))
    fd_produto = TenantForeignKey(
        verbose_name=_("produto"),
        to="produtos.Produto",
        on_delete=models.CASCADE,
        null=True,
        related_name="integracao_ifood",
    )

    class Meta:
        db_table = "produto_ifood"
        ordering = ["-id"]
        verbose_name = _("Produto do iFood")
        verbose_name_plural = _("Produtos do iFood")


class PedidoIfood:
    fd_ifood_id = models.UUIDField(_("id do pedido no iFood"))

    class Meta:
        db_table = "pedido_ifood"
        ordering = ["-id"]
        verbose_name = _("Pedido do iFood")
        verbose_name_plural = _("Pedidos do iFood")


class EventoIfood:
    vf_dados = models.JSONField(_("dados do evento"))

    class Meta:
        db_table = "evento_ifood"
        ordering = ["-id"]
        verbose_name = _("Evento do iFood")
        verbose_name_plural = _("Eventos do iFood")
