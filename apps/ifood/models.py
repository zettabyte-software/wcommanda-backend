from django.db import models
from django.utils.translation import gettext_lazy as _

from django_multitenant.fields import TenantForeignKey, TenantOneToOneField

from apps.system.base.models import Base


class StatusCategoriaIfood(models.TextChoices):
    AVAILABLE = "AVAILABLE"
    UNAVAILABLE = "UNAVAILABLE"


class TemplatesCategoriaIfood(models.TextChoices):
    PIZZA = "PIZZA"
    DEFAULT = "DEFAULT"


class CatalogIfood(Base):
    cc_ifood_id = models.UUIDField(_("id do iFood"), null=True)

    class Meta:
        db_table = "catalog_ifood"
        ordering = ["-id"]
        verbose_name = _("Catálog do iFood")
        verbose_name_plural = _("Catálogs do iFood")


class MerchantIfood:
    md_ifood_id = models.UUIDField(_("id do iFood"), null=True)

    class Meta:
        db_table = "merchant_ifood"
        ordering = ["-id"]
        verbose_name = _("Merchant do iFood")
        verbose_name_plural = _("Merchants do iFood")


class ProdutoIfood(Base):
    fd_produto = TenantOneToOneField(
        verbose_name=_("produto"),
        to="produtos.Produto",
        on_delete=models.CASCADE,
        related_name="integracao_ifood",
        unique=True,
    )
    fd_ifood_id = models.UUIDField(_("id ifood"), null=True)
    fd_pizza = models.BooleanField(_("é pizza"), default=False)
    fd_categoria_id = models.UUIDField(_("id do grupo do catálogo ifood"), null=True)
    fd_grupo_catalog_id = models.UUIDField(_("id do grupo do catálogo ifood"), null=True)
    fd_item_catalog_id = models.UUIDField(_("id do item no catálogo ifood"), null=True)
    fd_index = models.PositiveSmallIntegerField(_("posição no cardápio"), default=1)

    def __str__(self):
        return str(self.fd_ifood_id)

    class Meta:
        db_table = "dados_produto_ifood"
        ordering = ["-id"]
        verbose_name = _("Dados do Produto no iFood")
        verbose_name_plural = _("Dados dos Produtos no iFood")


class CategoriaIfood(Base):  # DadosCategoriaIfood
    cd_ifood_id = models.UUIDField(_("id iFood"), null=True)
    cd_categoria = TenantOneToOneField(
        verbose_name=_("categoria"),
        to="produtos.CategoriaProduto",
        on_delete=models.CASCADE,
        related_name="integracao_ifood",
        unique=True,
    )
    cd_template = models.CharField(_("template"), max_length=7, default=TemplatesCategoriaIfood.DEFAULT)
    cd_index = models.PositiveSmallIntegerField(_("index"), default=1)
    cd_sequence = models.PositiveSmallIntegerField(_("sequência"), default=1)

    def gerar_dados_ifood(self, id=False):
        dados = {
            "name": self.cd_categoria.cg_nome,
            "status": "AVAILABLE" if self.cd_categoria.ativo else "UNAVAILABLE",
            "template": self.cd_template,
            "sequence": self.cd_index,
            "index": self.cd_sequence,
        }

        if id:
            dados["id"] = str(self.cd_ifood_id)

        return dados

    def __str__(self):
        return str(self.cd_ifood_id)

    class Meta:
        db_table = "dados_categoria_ifood"
        ordering = ["-id"]
        verbose_name = _("Dados da Categoria do Produto do iFood")
        verbose_name_plural = _("Dados das Categoria dos Produtos do iFood")


class CustomizacaoCategoriaIfood:
    pass


class PedidoIfood(Base):
    fd_ifood_id = models.UUIDField(_("id do pedido no iFood"))
    fd_teste = models.BooleanField(_("é pedido de teste"), default=False)
    # fd_tipo_pedido = models.CharField(_("tipo do pedido"), max_length=8)

    # endereço
    fd_cep = models.CharField(_("cep"), max_length=8)
    fd_estado = models.CharField(_("estado"), max_length=2)
    fd_cidade = models.CharField(_("cidade"), max_length=40)
    fd_bairro = models.CharField(_("bairro"), max_length=30)
    fd_rua = models.CharField(_("rua"), max_length=15)
    fd_numero = models.CharField(_("número"), max_length=8)
    fd_complemento = models.CharField(_("complemento"), max_length=350, blank=True, default="")

    # daods do cliente
    fd_nome_cliente = models.CharField(_("nome do cliente"), max_length=120, blank=True, default="")
    fd_documento_cliente = models.CharField(_("documento do cliente"), max_length=20, blank=True, default="")
    fd_telefone_cliente = models.CharField(_("telefone do cliente"), max_length=15, blank=True, default="")

    class Meta:
        db_table = "pedido_ifood"
        ordering = ["-id"]
        verbose_name = _("Pedido do iFood")
        verbose_name_plural = _("Pedidos do iFood")


class PedidoItemIfood(Base):
    ft_pedido = TenantForeignKey(verbose_name=_("id interno"), to="ifood.PedidoIfood", on_delete=models.PROTECT, related_name="itens")
    ft_ifood_id = models.UUIDField(_("id do item do pedido no iFood"))
    ft_index = models.PositiveSmallIntegerField(_("index do item do pedido no iFood"), default=0)
    ft_pedido_ifood = models.UUIDField(_("id do pedido no iFood"))
    # ft_tipo_pedido = models.CharField(_("tipo do pedido"), max_length=8)

    ft_nome_produto = models.CharField(_("nome do produto"), max_length=80)
    fd_imagem_produto = models.URLField(_("complemento"), blank=True, default="")
    ft_unidade = models.CharField(_("unidade"), max_length=2)
    ft_preco_unitario = models.FloatField(_("preço unitário"), default=0)
    ft_quantidade = models.PositiveSmallIntegerField(_("quantidade"), default=0)
    ft_preco_total = models.FloatField(_("preço total"))
    ft_observacao = models.CharField(_("observação"), max_length=100, blank=True, default="")

    class Meta:
        db_table = "pedido_item_ifood"
        ordering = ["-id"]
        verbose_name = _("Item do Pedido do iFood")
        verbose_name_plural = _("Itens dos Pedidos do iFood")


class PedidoItemComplementoIfood(Base):
    pf_item_pedido = TenantForeignKey(verbose_name=_("id interno"), to="ifood.PedidoItemIfood", on_delete=models.PROTECT, related_name="complementos")
    pf_ifood_id = models.UUIDField(_("id do complemento do item no iFood"))
    pf_nome = models.CharField(_("nome"), max_length=150, default="")
    pf_quantidade = models.PositiveSmallIntegerField(_("quantidade"))
    pf_tipo = models.CharField(_("unidade"), max_length=20, default="")
    pf_preco_unitario = models.FloatField(_("preço unitário"))
    pf_preco = models.FloatField(_("preço total"))

    class Meta:
        db_table = "pedido_item_customizacao_ifood"
        ordering = ["-id"]
        verbose_name = _("Customização do Item do Pedido do iFood")
        verbose_name_plural = _("Customizações dos Itens dos Pedidos do iFood")
