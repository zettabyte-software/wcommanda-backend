from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from django_multitenant.fields import TenantForeignKey

from apps.system.base.models import Base
from apps.system.conf.services import get_configuracao


class StatusComandaChoices(models.IntegerChoices):
    ABERTA = 1, _("Aberta")
    FINALIZADA = 2, _("Finalizada")
    CANCELADA = 3, _("Cancelada")


class StatusComandaItemChoices(models.IntegerChoices):
    ABERTO = 1, _("Aberto")
    PREPARANDO = 2, _("Preparando")
    PRONTO = 3, _("Pronto")
    ENTREGUE = 4, _("Entregue")
    CANCELADO = 5, _("Cancelado")


class FormasPagamentoComandaChoices(models.IntegerChoices):
    CARTAO_CREDITO = 1, _("Cartão de Crédito")
    CARTAO_DEBITO = 2, _("Cartão de Débito")
    DINHEIRO = 3, _("Dinheiro")
    PIX = 4, _("PIX")
    OUTRO = 99, _("Outro")


class Comanda(Base):
    # TODO gerar um QR code para uma página onde a pessoa pode acompanhar se o pedido está pronto
    cm_codigo = models.PositiveSmallIntegerField(_("código"), editable=False, default=1)
    cm_status = models.PositiveSmallIntegerField(
        _("status"),
        choices=StatusComandaChoices.choices,
        default=StatusComandaChoices.ABERTA
    )
    cm_mesa = TenantForeignKey(
        verbose_name=_("mesa"),
        to="mesas.Mesa",
        on_delete=models.PROTECT,
        null=True,
        related_name="comandas",
    )
    cm_garcom = TenantForeignKey(
        verbose_name=_("garçom"),
        to=settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        null=True,
        related_name="comandas",
    )
    # TODO criar uma referencia do cliente para poder mostrar um histórico do que ele já pediu + recomendações baseado nas categorias dos produtos que ele já pediu
    cm_cliente = models.CharField(_("cliente"), max_length=30, blank=True)
    cm_cliente_fidelidade = TenantForeignKey(
        verbose_name=_("cliente fidelidade"),
        to="clientes.Cliente",
        on_delete=models.PROTECT,
        null=True,
    )
    cm_cartao_fidelidade = TenantForeignKey(
        verbose_name=_("cartão fidelidade resgatado"),
        to="fidelidade.CartaoFidelidade",
        on_delete=models.PROTECT,
        null=True,
    )
    cm_forma_pagamento = models.PositiveSmallIntegerField(
        _("forma de pagamento"),
        choices=FormasPagamentoComandaChoices.choices,
        null=True,
    )

    cm_data_finalizacao = models.DateField(_("data da finalização"), null=True)
    cm_hora_finalizacao = models.TimeField(_("hora da finalização"), null=True)

    cm_data_cancelamento = models.DateField(_("data do cancelamento"), null=True)
    cm_hora_cancelamento = models.TimeField(_("hora do cancelamento"), null=True)
    cm_motivo_cancelamento = models.CharField(_("motivo do cancelamento"), max_length=50, blank=True)

    cm_cupon = TenantForeignKey(
        verbose_name=_("cupon"),
        to="descontos.CuponDesconto",
        on_delete=models.PROTECT,
        null=True,
    )

    @property
    def cm_valor_total(self):
        valor_total = (
            self.itens.filter(  # type: ignore
                ct_comanda=self,
            )
            .exclude(
                ct_status=StatusComandaChoices.CANCELADA,
            )
            .aggregate(total=models.Sum(models.F("ct_preco_unitario_produto")))["total"]
            or 0
        )

        try:
            if self.cm_cupon:
                return self.cm_cupon.get_valor_com_desconto(valor_total)
        except ValueError:
            pass

        return round(valor_total, 2)

    @property
    def cm_valor_comissao(self):
        percentual = round(get_configuracao("WCM_PERCENTUAL_COMISSAO_GARCON") / 100, 2)
        return round(self.cm_valor_total * percentual, 2)

    class Meta:
        db_table = "comanda"
        ordering = ["-id"]
        verbose_name = _("Comanda")
        verbose_name_plural = _("Comandas")


class ComandaItem(Base):
    ct_status = models.PositiveSmallIntegerField(
        _("status"),
        choices=StatusComandaItemChoices.choices,
        default=StatusComandaItemChoices.ABERTO,
    )
    ct_comanda = TenantForeignKey(
        verbose_name=_("comanda"),
        to="comandas.Comanda",
        on_delete=models.CASCADE,
        related_name="itens",
    )
    ct_pedido = models.PositiveSmallIntegerField(_("sequência"), default=0)
    ct_produto = TenantForeignKey(
        verbose_name=_("produto"),
        to="produtos.Produto",
        on_delete=models.PROTECT,
        related_name="comanda_itens",
    )
    ct_preco_unitario_produto = models.FloatField(_("preço unitário do produto"), default=0)

    ct_premio = models.BooleanField(_("é um prêmio"), default=False)

    ct_data_preparamento = models.DateField(_("data do preparamento"), null=True)
    ct_hora_preparamento = models.TimeField(_("hora do preparamento"), null=True)

    ct_data_finalizacao = models.DateField(_("data da finalização"), null=True)
    ct_hora_finalizacao = models.TimeField(_("hora da finalização"), null=True)

    ct_data_entregue = models.DateField(_("data da entrega ao cliente"), null=True)
    ct_hora_entregue = models.TimeField(_("hora da entrega ao cliente"), null=True)

    ct_observacao = models.CharField(_("observação"), max_length=100, blank=True)

    class Meta:
        db_table = "comanda_item"
        ordering = ["-id"]
        verbose_name = _("Item da Comanda")
        verbose_name_plural = _("Items da Comanda")
