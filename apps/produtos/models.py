import random

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from django.utils.translation import gettext_lazy as _

from django_multitenant.fields import TenantForeignKey
from django_multitenant.utils import get_current_tenant

from apps.comandas.models import StatusComandaItemChoices
from apps.system.base.models import Base
from lib.cloudflare.bucket import R2CloudflareHandler
from utils.env import get_env_var


class TiposChoices(models.IntegerChoices):
    PREPARAVEL = 1, _("Preparável")
    CONSUMIVEL = 2, _("Consumível")
    ADICIONAL = 3, _("Adicional")


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

    pr_imagem = models.URLField(_("foto"), blank=True, default="")

    bucket_client = R2CloudflareHandler()

    @classmethod
    def upload(cls, produto: "Produto", image: InMemoryUploadedFile):
        tenant = get_current_tenant()
        file_extension = image.name.split(".")[-1]
        new_file_name = random.randint(1000000, 9999999)

        path = f"{tenant.pk}/img/produtos/{produto.pk}/{new_file_name}.{file_extension}"

        cls.bucket_client.upload(image, path)

        url = get_env_var("CLOUDFLARE_R2_BUCKET_URL")
        bucket = get_env_var("CLOUDFLARE_R2_BUCKET")

        full_url = f"{url}/{bucket}/{path}"

        produto.pr_imagem = full_url
        produto.save()

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
        verbose_name = _("Imagem do Produto")
        verbose_name_plural = _("Imagens dos Produtos")


class Acrescimo(Base):
    cs_nome = models.CharField(_("nome"), max_length=40)
    cs_preco = models.FloatField(_("preço"), default=0)
    cs_descricao = models.CharField(_("descrição"), max_length=50, blank=True)

    class Meta:
        db_table = "acresimo"
        ordering = ["-id"]
        verbose_name = _("Acréscimo")
        verbose_name_plural = _("Acréscimos")


class AcrescimoProduto(Base):
    cp_produto = TenantForeignKey(
        verbose_name=_("produto"),
        to="produtos.Produto",
        on_delete=models.CASCADE,
        related_name="acrescimos",
    )

    cp_acrescimo = TenantForeignKey(
        verbose_name=_("acréscimo"),
        to="produtos.Acrescimo",
        on_delete=models.CASCADE,
    )

    def __str__(self) -> str:
        return f"{self.cp_produto.pr_nome} - {self.cp_acrescimo.cs_nome}"

    class Meta:
        db_table = "acresimo_produto"
        ordering = ["-id"]
        verbose_name = _("Acréscimo do Produto")
        verbose_name_plural = _("Acréscimos dos Produtos")


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
