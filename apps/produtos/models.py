import uuid

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.validators import MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from django_multitenant.fields import TenantForeignKey
from django_multitenant.utils import get_current_tenant

from apps.comandas.models import StatusComandaItemChoices
from apps.system.base.models import Base
from lib.back_blaze.bucket import BackBlazeB2Handler
from utils.env import get_env_var

DEFAULT_BUCKET_PHOTO_PATH = '%s/produtos/%s/imgs/%s'
"""Caminho padrão para a imagem dentro do bucket: \n
<id_tenant>/produtos/<id_produto>/imgs/<nome_arquivo>
"""


class TiposChoices(models.IntegerChoices):
    PREPARAVEL = 1, _("Preparável")
    CONSUMIVEL = 2, _("Consumível")


class UnidadesProdutoChoices(models.IntegerChoices):
    GRAMA = 1, _("Grama")
    QUILO = 2, _("Quilo")
    MILILITRO = 3, _("Mililitro")
    LITRO = 4, _("Litro")
    UNIDADE = 5, _("Unidade")
    FATIA = 6, _("Fatia")
    PORCAO = 7, _("Porção")
    OUTRO = 99, _("Outra")


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

    pr_path_imagem = models.CharField(_("foto"), max_length=40, blank=True, default="")
    pr_id_back_blaze = models.CharField(_("foto"), max_length=40, blank=True, default="")

    # restrições alimentares
    pr_vegano = models.BooleanField(_("vegano"), default=False)
    pr_vegetariano = models.BooleanField(_("vegetariano"), default=False)
    pr_organico = models.BooleanField(_("orgânico"), default=False)
    pr_sem_gluten = models.BooleanField(_("sem glúten"), default=False)
    pr_sem_acucar = models.BooleanField(_("sem açúcar"), default=False)
    pr_zero_lactose = models.BooleanField(_("zero lactose"), default=False)

    # complemento
    pr_grupo_complementos = TenantForeignKey(
        verbose_name=_("grupo de complementos"),
        to="produtos.GrupoComplementoProduto",
        on_delete=models.PROTECT,
        null=True,
        related_name="produtos",
    )

    # porção da comida
    pr_serve_pessoas = models.PositiveSmallIntegerField(_("n° de pessoas que a comida serve"), validators=[MaxValueValidator(4)], null=True)
    pr_unidade = models.PositiveSmallIntegerField(_("tipo"), choices=UnidadesProdutoChoices.choices, null=True)
    pr_quantidade = models.IntegerField(_("tipo"), default=0)

    # pr_integra_ifood = models.BooleanField(_("integra com o ifood"), default=False)

    @property
    def pr_url_imagem(self):
        if not self.pr_path_imagem:
            return None

        bucket = get_env_var("BACKBLAZE_BUCKET_NAME")
        return f'https://f005.backblazeb2.com/file/{bucket}/{self.pr_path_imagem}'

    @classmethod
    def upload(cls, produto: "Produto", arquivo: InMemoryUploadedFile, metadata="{}"):
        handler = BackBlazeB2Handler()
        assinatura = get_current_tenant()
        nome_aleatorio_imagem = str(uuid.uuid4())

        path = DEFAULT_BUCKET_PHOTO_PATH % (
            assinatura.ss_codigo_licenca,  # type: ignore
            produto.pk,
            nome_aleatorio_imagem,
        )

        file_version = handler.upload(arquivo.read(), path, metadata)

        produto.pr_path_imagem = path
        produto.pr_id_back_blaze = file_version.id_
        produto.save()

    @classmethod
    def remover_foto(cls, produto: "Produto"):
        handler = BackBlazeB2Handler()
        produto.pr_path_imagem = ""
        produto.pr_id_back_blaze = ""
        produto.save()
        return handler.destroy(produto.pr_id_back_blaze, produto.pr_path_imagem)

    class Meta:
        db_table = "produto"
        ordering = ["-id"]
        verbose_name = _("Produto")
        verbose_name_plural = _("Produtos")


class CategoriaProduto(Base):
    cg_nome = models.CharField(_("nome"), max_length=30)
    cg_descricao = models.CharField(_("descrição"), max_length=100, blank=True, default="")
    # cg_integra_ifood = models.BooleanField(_("integra com o ifood"), default=False)

    class Meta:
        db_table = "categoria_produto"
        ordering = ["-id"]
        verbose_name = _("Categoria")
        verbose_name_plural = _("Categorias")


class GrupoComplementoProduto(Base):
    gr_nome = models.CharField(_("nome"), max_length=30)

    class Meta:
        db_table = "grupo_complemento_produto"
        ordering = ["-id"]
        verbose_name = _("Grupo de Acréscimo do Produto")
        verbose_name_plural = _("Grupos de Acréscimos dos Produtos")


class ComplementoProduto(Base):
    pc_grupo_complemento = TenantForeignKey(
        verbose_name=_("grupo de complemento"),
        to="produtos.GrupoComplementoProduto",
        on_delete=models.CASCADE,
        related_name="complementos",
    )
    pc_nome = models.CharField(_("nome"), max_length=40)
    pc_preco = models.FloatField(_("preço"), default=0)
    pc_quantidade_minima = models.FloatField(_("quantidade máxima"), default=1)
    pc_quantidade_maxima = models.FloatField(_("quantidade máxima"), default=1)
    pc_descricao = models.CharField(_("descrição"), max_length=50, blank=True)
    pc_obrigatorio = models.BooleanField(_("obrigatório"), default=False)

    class Meta:
        db_table = "complemento_produto"
        ordering = ["-id"]
        verbose_name = _("Complemento do Produto")
        verbose_name_plural = _("Complementos dos Produtos")
