import uuid

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from django_multitenant.fields import TenantForeignKey
from threadlocals.threadlocals import get_current_request

from apps.system.base.models import Base
from apps.system.tenants.services import get_current_token


def gerar_codigo_cupon_aleatorio(*args):
    return str(uuid.uuid4())[:7].upper()


class StatusCartaoFidelidadeChoices(models.TextChoices):
    ABERTA = "ABE", _("Aberto")
    COMPLETO = "COM", _("Completo")
    RESGATADA = "RES", _("Resgatado")
    CANCELADA = "CAN", _("Cancelado")


class CartaoFidelidade(Base):
    class OPCOES_STATUS:
        ABERTA = "ABE"
        COMPLETO = "COM"
        RESGATADA = "RES"
        CANCELADA = "CAN"

    cr_codigo = models.CharField(
        _("código"),
        max_length=10,
        default=gerar_codigo_cupon_aleatorio,
    )
    cr_status = models.CharField(
        _("status"),
        max_length=3,
        default=OPCOES_STATUS.ABERTA,
    )
    cr_cliente = TenantForeignKey(
        verbose_name=_("cliente"),
        to="clientes.Cliente",
        on_delete=models.PROTECT,
        related_name="cartoes_fidelidade",
    )
    cr_expiracao = models.DateField(_("data de expiração"))
    cr_premio = TenantForeignKey(
        verbose_name=_("prêmio"),
        to="fidelidade.Premio",
        on_delete=models.PROTECT,
        related_name="cartoes_fidelidade",
    )
    cr_condicao_premio = TenantForeignKey(
        verbose_name=_("condição da premio"),
        to="fidelidade.CondicaoPremio",
        on_delete=models.PROTECT,
        related_name="cartoes_fidelidade",
    )
    cr_filial = TenantForeignKey(
        verbose_name=_("filial"),
        to="filiais.Filial",
        on_delete=models.PROTECT,
        related_name="cartoes_fidelidade",
    )

    @property
    def cr_total_carimbos(self):
        return Carimbo.objects.filter(cb_cartao_fidelidade=self).count()

    @property
    def cr_expirado(self):
        hoje = timezone.now().date()
        return hoje > self.cr_expiracao

    @property
    def cr_link(self):
        request = get_current_request()
        host = request.headers.get(settings.TENANT_HOST_HEADER)
        token = get_current_token()
        link = f"https://{host}/sespaco-do-cliente/cartoes-fidelidade/{self.pk}/?jwt={token}"
        return link

    class Meta:
        db_table = "cartao_fidelidade"
        ordering = ["-id"]
        verbose_name = _("Cartão Fidelidade")
        verbose_name_plural = _("Cartões Fidelidade")


class Carimbo(Base):
    cb_cartao_fidelidade = TenantForeignKey(
        verbose_name=_("cartão fidelidade"),
        to="fidelidade.CartaoFidelidade",
        on_delete=models.CASCADE,
        related_name="carimbos",
    )

    class Meta:
        db_table = "carimbo"
        ordering = ["-id"]
        verbose_name = _("Carimbo")
        verbose_name_plural = _("Carimbos")


class Premio(Base):
    pm_nome = models.CharField(_("nome"), max_length=50)
    pm_descricao = models.CharField(
        _("descrição"), max_length=150, blank=True, default=""
    )

    class Meta:
        db_table = "premio"
        ordering = ["-id"]
        verbose_name = _("Prêmio")
        verbose_name_plural = _("Prêmios")


class PremioItem(Base):
    pt_premio = TenantForeignKey(
        verbose_name=_("cliente"),
        to="fidelidade.Premio",
        on_delete=models.CASCADE,
        related_name="itens",
    )
    pt_produto = TenantForeignKey(
        verbose_name=_("produto"),
        to="produtos.Produto",
        on_delete=models.PROTECT,
        related_name="premios",
    )
    pt_observacao = models.CharField(
        _("observação"), max_length=150, blank=True, default=""
    )

    class Meta:
        db_table = "premio_item"
        ordering = ["-id"]
        verbose_name = _("Item do Prêmio")
        verbose_name_plural = _("Itens do Prêmios")


class CondicaoPremio(Base):
    cn_nome = models.CharField(_("nome"), max_length=25)
    cn_quantidade = models.PositiveSmallIntegerField(
        _("quantidade"),
        default=1,
        null=True,
    )
    cn_valor_minimo = models.FloatField(
        _("valor mínimo"),
        default=1,
        null=True,
    )
    cn_produto = TenantForeignKey(
        verbose_name=_("produto"),
        to="produtos.Produto",
        on_delete=models.PROTECT,
        null=True,
    )

    class Meta:
        db_table = "condicao_premio"
        ordering = ["-id"]
        verbose_name = _("Condição da Prêmio")
        verbose_name_plural = _("Condições dos Prêmios")
