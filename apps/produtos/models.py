import base64
import random

from django.db import models
from django.utils.translation import gettext_lazy as _

from django_multitenant.fields import TenantForeignKey
from django_multitenant.utils import get_current_tenant

from apps.comandas.models import StatusComandaItemChoices
from apps.system.base.models import Base


class TiposChoices(models.IntegerChoices):
    PREPARAVEL = 1, _("Preparável")
    CONSUMIVEL = 2, _("Consumível")


class Produto(Base):
    pr_tipo = models.PositiveSmallIntegerField(_("tipo"), choices=TiposChoices.choices, default=TiposChoices.CONSUMIVEL)
    pr_nome = models.CharField(_("nome"), max_length=100)
    pr_codigo_cardapio = models.CharField(_("código do cardápio"), max_length=8)
    pr_preco = models.FloatField(_("preço"), default=0)
    pr_tempo_preparo = models.IntegerField(_("código"), default=0)
    pr_categoria = TenantForeignKey(
        verbose_name=_("categoria"),
        to="produtos.CategoriaProduto",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )
    pr_descricao = models.TextField(_("descrição"), blank=True, default="")
    pr_controla_estoque = models.BooleanField(_("controla estoque"), default=False)
    pr_status_padrao_comanda_item = models.PositiveSmallIntegerField(
        _("tipo"),
        choices=StatusComandaItemChoices.choices,
        default=StatusComandaItemChoices.ABERTO,
    )

    def make_upload_path(self, filename):
        file_extension = filename.split(".")[-1]
        new_file_name = random.randint(1000000, 9999999)
        tenant = get_current_tenant()
        return f"{tenant.pk}/produtos/{new_file_name}.{file_extension}"

    pr_imagem = models.ImageField(_("foto"), upload_to=make_upload_path, blank=True, null=True)  # type: ignore

    @property
    def pr_imagem_base64(self):
        if self.pr_imagem:
            file = open(self.pr_imagem.path, "rb")
            image_data = file.read()
            base64_image = base64.b64encode(image_data).decode("utf-8")
            return base64_image
        else:
            return None

    class Meta:
        db_table = "produto"
        ordering = ["-id"]
        verbose_name = _("Produto")
        verbose_name_plural = _("Produtos")


class ImagemProduto:
    mg_produto = TenantForeignKey(
        verbose_name=_("produto"),
        to="produtos.Produto",
        on_delete=models.CASCADE,
    )
    mg_imagem = models.ImageField(_("imagem"))

    class Meta:
        db_table = "imagem_produto"
        ordering = ["-id"]
        verbose_name = _("Produto")
        verbose_name_plural = _("Produtos")


class CategoriaProduto(Base):
    cg_nome = models.CharField(_("nome"), max_length=30)
    cg_descricao = models.CharField(_("descrição"), max_length=100, blank=True)

    class Meta:
        db_table = "categoria_produto"
        ordering = ["-id"]
        verbose_name = _("Categoria")
        verbose_name_plural = _("Categorias")


class Ingrediente:
    ng_nome = models.CharField(_("nome"), max_length=50)
    ng_preco = models.FloatField(_("preço"), default=0)
    ng_descricao = models.CharField(_("descrição"), max_length=700, blank=True)
    ng_quantidade = models.FloatField(verbose_name=_("quantidade"))

    class Meta:
        db_table = "ingrediente_produto"
        ordering = ["-id"]
        verbose_name = _("Ingrediente")
        verbose_name_plural = _("Ingredientes")
