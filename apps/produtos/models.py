import uuid

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.validators import MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from auditlog.registry import auditlog
from django_multitenant.fields import TenantForeignKey
from django_multitenant.utils import get_current_tenant

from apps.comandas.models import StatusComandaItemChoices
from apps.system.base.models import Base
from lib.back_blaze.bucket import BackBlazeB2Handler

DEFAULT_BUCKET_PRODUCT_PHOTO_PATH = "%s/produtos/%s/imgs/%s"
"""Caminho padrão para a imagem dentro do bucket: \n
[id_tenant]/produtos/[id_produto]/imgs/[nome_arquivo]
"""


class TiposChoices(models.IntegerChoices):
    PREPARAVEL = 1, _("Preparável")
    CONSUMIVEL = 2, _("Consumível")


class PontosCarneChoices(models.IntegerChoices):
    NAO_TEM = 0, _("Não tem ponto")
    MAL_PASSADA = 1, _("Mal passada")
    AO_PONTO_PARA_MAL_PASSADA = 2, _("Ao ponto para mal passada")
    AO_PONTO = 3, _("Ao ponto")
    AO_PONTO_PARA_BEM_PASSADA = 4, _("Ao ponto para bem passada")
    BEM_PASSADA = 5, _("Bem passada")


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
    pr_codigo_cardapio = models.CharField(_("código do cardápio"), max_length=8, blank=True, default="")
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

    pr_url_imagem = models.URLField(_("url amigável da foto"), blank=True, default="")
    pr_path_imagem = models.CharField(_("caminho da imagem no bucket"), max_length=120, blank=True, default="")
    pr_id_back_blaze = models.CharField(_("id backblaze do upload"), max_length=102, blank=True, default="")

    # restrições alimentares
    pr_vegano = models.BooleanField(_("vegano"), default=False)
    pr_vegetariano = models.BooleanField(_("vegetariano"), default=False)
    pr_organico = models.BooleanField(_("orgânico"), default=False)
    pr_sem_gluten = models.BooleanField(_("sem glúten"), default=False)
    pr_sem_acucar = models.BooleanField(_("sem açúcar"), default=False)
    pr_zero_lactose = models.BooleanField(_("zero lactose"), default=False)

    # complemento
    # pr_grupo_complementos = TenantForeignKey(
    #     verbose_name=_("grupo de complementos"),
    #     to="produtos.GrupoComplementoProduto",
    #     on_delete=models.PROTECT,
    #     null=True,
    #     related_name="produtos",
    # )

    # porção da comida
    pr_serve_pessoas = models.PositiveSmallIntegerField(
        _("n° de pessoas que a comida serve"), validators=[MaxValueValidator(4)], null=True
    )
    pr_unidade = models.PositiveSmallIntegerField(_("tipo"), choices=UnidadesProdutoChoices.choices, null=True)
    pr_quantidade = models.PositiveSmallIntegerField(_("tipo"), default=0)

    @classmethod
    def upload(cls, produto: "Produto", arquivo: InMemoryUploadedFile, metadata=None):
        if metadata is None:
            metadata = {}

        handler = BackBlazeB2Handler()
        assinatura = get_current_tenant()
        extencao = arquivo.name.split(".")[-1]
        nome_aleatorio_imagem = f'{uuid.uuid4()}.{extencao}'

        path = DEFAULT_BUCKET_PRODUCT_PHOTO_PATH % (
            assinatura.ss_codigo_licenca,  # type: ignore
            produto.pk,
            nome_aleatorio_imagem,
        )

        file_version = handler.upload(arquivo.read(), path, metadata)

        produto.pr_path_imagem = path
        produto.pr_id_back_blaze = file_version.id_
        produto.pr_url_imagem = f"https://f005.backblazeb2.com/file/wcommanda/{path}"

        produto.save()

    @classmethod
    def remover_foto(cls, produto: "Produto"):
        handler = BackBlazeB2Handler()
        handler.destroy(produto.pr_id_back_blaze, produto.pr_path_imagem)

        produto.pr_url_imagem = ""
        produto.pr_path_imagem = ""
        produto.pr_id_back_blaze = ""

        produto.save()

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


class CustomizacaoProduto(Base):
    cz_produto = TenantForeignKey(
        verbose_name=_("produto"),
        to="produtos.Produto",
        on_delete=models.CASCADE,
        related_name="customizacoes",
    )
    cz_nome = models.CharField(_("nome"), max_length=30)
    cz_preco = models.FloatField(_("preço"), default=0)
    cz_descricao = models.CharField(_("descrição"), max_length=150, blank=True)

    class Meta:
        db_table = "customizacao_produto"
        ordering = ["-id"]
        verbose_name = _("Customização do Produto")
        verbose_name_plural = _("Customizações dos Produtos")


class CustomizacaoProdutoItem(Base):
    cc_customizacao = TenantForeignKey(
        verbose_name=_("customização"),
        to="produtos.CustomizacaoProduto",
        on_delete=models.CASCADE,
        related_name="itens",
    )
    cc_nome = models.CharField(_("nome"), max_length=30)
    cc_descricao = models.CharField(_("descrição"), max_length=150, blank=True)

    class Meta:
        db_table = "customizacao_produto_item"
        ordering = ["-id"]
        verbose_name = _("Item da Customização do Produto")
        verbose_name_plural = _("Itens das Customizações dos Produtos")


# class GrupoComplementoProduto(Base):
#     gr_nome = models.CharField(_("nome"), max_length=30)

#     class Meta:
#         db_table = "grupo_complemento_produto"
#         ordering = ["-id"]
#         verbose_name = _("Grupo de Acréscimo do Produto")
#         verbose_name_plural = _("Grupos de Acréscimos dos Produtos")


# class ComplementoProduto(Base):
#     pc_grupo_complemento = TenantForeignKey(
#         verbose_name=_("grupo de complemento"),
#         to="produtos.GrupoComplementoProduto",
#         on_delete=models.CASCADE,
#         related_name="complementos",
#     )
#     pc_nome = models.CharField(_("nome"), max_length=40)
#     pc_preco = models.FloatField(_("preço"), default=0)
#     pc_quantidade_minima = models.FloatField(_("quantidade máxima"), default=1)
#     pc_quantidade_maxima = models.FloatField(_("quantidade máxima"), default=1)
#     pc_descricao = models.CharField(_("descrição"), max_length=50, blank=True)
#     pc_obrigatorio = models.BooleanField(_("obrigatório"), default=False)

#     class Meta:
#         db_table = "complemento_produto"
#         ordering = ["-id"]
#         verbose_name = _("Complemento do Produto")
#         verbose_name_plural = _("Complementos dos Produtos")


auditlog.register(
    Produto,
    exclude_fields=[
        "data_ultima_alteracao",
        "hora_ultima_alteracao",
    ],
)
auditlog.register(
    CategoriaProduto,
    exclude_fields=[
        "data_ultima_alteracao",
        "hora_ultima_alteracao",
    ],
)
# auditlog.register(
#     GrupoComplementoProduto,
#     exclude_fields=[
#         "data_ultima_alteracao",
#         "hora_ultima_alteracao",
#     ],
# )
# auditlog.register(
#     ComplementoProduto,
#     exclude_fields=[
#         "data_ultima_alteracao",
#         "hora_ultima_alteracao",
#     ],
# )
