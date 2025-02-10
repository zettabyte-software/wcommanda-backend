from django.db import models
from django.utils.translation import gettext_lazy as _

from auditlog.registry import auditlog
from django_multitenant.fields import TenantForeignKey

from apps.system.base.models import Base


class TiposMovimentacaoEstoqueChoices(models.IntegerChoices):
    ENTRADA = 1, _("Entrada")
    SAIDA = 2, _("Saída")


class MovimentacaoEstoque(Base):
    mv_comanda_item = TenantForeignKey(
        verbose_name=_("comanda item"),
        to="comandas.ComandaItem",
        on_delete=models.PROTECT,
        related_name="movimentacoes",
        null=True,
    )
    mv_tipo = models.PositiveSmallIntegerField(_("tipo"), choices=TiposMovimentacaoEstoqueChoices.choices)
    mv_produto = TenantForeignKey(
        verbose_name=_("produto gerado"),
        to="produtos.Produto",
        on_delete=models.PROTECT,
        related_name="movimentacoes",
        null=True,
    )
    mv_quantidade = models.FloatField(_("quantidade"), default=0)
    mv_quantidade_anterior = models.FloatField(_("quantidade anterior"), default=0)
    mv_quantidade_atual = models.FloatField(_("quantidade atual"), default=0)

    class Meta:
        db_table = "movimentacao_estoque"
        ordering = ["-id"]
        verbose_name = _("Movimentação de Estoque do Produto")
        verbose_name_plural = _("Movimentações de Estoque dos Produtos")


auditlog.register(
    MovimentacaoEstoque,
    exclude_fields=[
        "data_ultima_alteracao",
        "hora_ultima_alteracao",
    ],
)
