from django.db import models
from django.utils.translation import gettext_lazy as _

from django_multitenant.fields import TenantForeignKey

from apps.system.base.models import Base


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
    fd_teste = models.BooleanField(_("é pedido de teste"), default=False)
    fd_tipo_pedido = models.CharField(_("tipo do pedido"), max_length=8)

    fd_cep = models.CharField(_("cep"), max_length=8)
    fd_estado = models.CharField(_("estado"), max_length=2)
    fd_cidade = models.CharField(_("cidade"), max_length=40)
    fd_bairro = models.CharField(_("bairro"), max_length=30)
    fd_rua = models.CharField(_("rua"), max_length=15)
    fd_numero = models.CharField(_("número"), max_length=8)
    fd_complemento = models.CharField(_("complemento"), max_length=50, blank=True, default="")

    class Meta:
        db_table = "pedido_ifood"
        ordering = ["-id"]
        verbose_name = _("Pedido do iFood")
        verbose_name_plural = _("Pedidos do iFood")


class PedidoItemIfood:
    ft_ifood_id = models.UUIDField(_("id do pedido no iFood"))
    ft_nome_produto = models.CharField(_("nome do produto"), max_length=80)
    ft_unidade = models.CharField(_("unidade"), max_length=2)
    ft_pedido = models.UUIDField(_("id do pedido no iFood"))
    ft_tipo_pedido = models.CharField(_("tipo do pedido"), max_length=8)
    ft_preco_unitario = models.FloatField(_("preço unitário"))
    ft_quantidade = models.PositiveSmallIntegerField(_("quantidade"))
    ft_preco_total = models.FloatField(_("preço total"))
    ft_observacao = models.CharField(_("observação"), max_length=100, blank=True, default="")

    class Meta:
        db_table = "pedido_item_ifood"
        ordering = ["-id"]
        verbose_name = _("Item do Pedido do iFood")
        verbose_name_plural = _("Itens dos Pedidos do iFood")


class PedidoItemCustomizacaoIfood:
    class Meta:
        db_table = "pedido_item_customizacao_ifood"
        ordering = ["-id"]
        verbose_name = _("Item do Pedido do iFood")
        verbose_name_plural = _("Itens dos Pedidos do iFood")
