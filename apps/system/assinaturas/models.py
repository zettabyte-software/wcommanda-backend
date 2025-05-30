import re
import uuid

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from django_multitenant.fields import TenantForeignKey
from django_multitenant.models import TenantModel

from apps.system.base.models import Base


def validar_subdominio(valor):
    subdominios_proibidos = ["www", "app", "admin", "mail"]

    if len(valor) > 30:
        raise ValidationError(_("O subdomínio deve ter no máximo 30 caracteres."))

    regex = r"^[a-zA-Z0-9]+(-[a-zA-Z0-9]+)*$"
    if not re.match(regex, valor):
        raise ValidationError(
            _(
                "Subdomínio inválido. Apenas letras, números e hífens são permitidos, "
                "e deve começar e terminar com uma letra ou número."
            )
        )

    if valor in subdominios_proibidos:
        raise ValidationError(_("O subdomínio fornecido é proibido."))


class StatusChoices(models.IntegerChoices):
    NORMAL = 0, _("Normal")
    CANCELADA = 1, _("Cancelada")
    ATRASADA = 2, _("Pagamento Atrasado")
    ULTRA = 99, _("Ultra(não precisa pagar)")


class TierChoices(models.IntegerChoices):
    TIER_1 = 1
    TIER_2 = 2
    TIER_3 = 3
    TIER_4 = 4


class Assinatura(TenantModel):
    tenant_id = "id"

    ss_nome = models.CharField(_("nome"), max_length=30)
    ss_subdominio = models.CharField(_("subdominio"), max_length=50)
    ss_cloudflare_id = models.CharField(_("id cloudflare"), max_length=50)
    ss_codigo_licenca = models.UUIDField(_("código da licença"), default=uuid.uuid4, editable=False)
    ss_status = models.IntegerField(_("status"), choices=StatusChoices.choices, default=StatusChoices.NORMAL)
    ss_plano = TenantForeignKey(
        verbose_name=_("plano"), to="assinaturas.Plano", on_delete=models.PROTECT, related_name="assinaturas"
    )

    # campos base
    data_criacao = models.DateField(_("data de criação"), auto_now_add=True)
    hora_criacao = models.TimeField(_("hora de criação"), auto_now_add=True)
    data_ultima_alteracao = models.DateField(_("data da última alteração"), auto_now=True)
    hora_ultima_alteracao = models.TimeField(_("hora da última alteração"), auto_now=True)

    class Meta:
        db_table = "assinatura"
        ordering = ["-id"]
        verbose_name = _("Assinatura")
        verbose_name_plural = _("Assinaturas")


class Plano(Base):
    ativo = None
    codigo = None
    filial = None
    owner = None
    assinatura = None

    pl_nome = models.CharField(_("nome"), max_length=15)
    pl_tier = models.PositiveIntegerField(_("tíer"), choices=TierChoices.choices, default=TierChoices.TIER_4)
    pl_numero_usuarios = models.PositiveIntegerField(_("número usuarios"), default=2)
    pl_valor_mensalidade = models.FloatField(_("valor da mensalidade"), default=0)
    pl_numero_telas = models.PositiveIntegerField(_("número de telas"), default=1)

    pl_integra_ifood = models.BooleanField(_("integra com o ifood"), default=False)
    pl_limite_integracoes_pedidos_ifood = models.PositiveIntegerField(
        _("número máximo pedidos de ifood recebíveis por mês"), default=0
    )

    pl_envia_sms = models.BooleanField(_("envia sms"), default=False)
    pl_limite_sms = models.PositiveIntegerField(_("número máximo sms por mês"), default=0)
    pl_saldo_sms = models.PositiveIntegerField(_("saldo restante dos sms por mês"), default=0)

    pl_observacao = models.CharField(_("observações"), max_length=50)

    @classmethod
    def criar_plano(cls, tier: TierChoices):
        if tier == TierChoices.TIER_1:
            return cls.criar_plano_basico()

        if tier == TierChoices.TIER_2:
            return cls.criar_plano_premium()

        if tier == TierChoices.TIER_3:
            return cls.criar_plano_pro()

        raise ValueError("Tíer inválido")

    @classmethod
    def criar_plano_basico(cls):
        return cls.objects.create(
            pl_nome="Básico",
            pl_tier=TierChoices.TIER_1,
            pl_numero_usuarios=3,
            pl_numero_integracoes_ifood=0,
            pl_valor_mensalidade=80,
            pl_observacao="",
        )

    @classmethod
    def criar_plano_premium(cls):
        return cls.objects.create(
            pl_nome="Prêmium",
            pl_tier=TierChoices.TIER_2,
            pl_numero_usuarios=7,
            pl_numero_integracoes_ifood=200,
            pl_valor_mensalidade=250,
            pl_observacao="",
        )

    @classmethod
    def criar_plano_pro(cls):
        return cls.objects.create(
            pl_nome="Pro",
            pl_tier=TierChoices.TIER_3,
            pl_numero_usuarios=15,
            pl_numero_integracoes_ifood=350,
            pl_valor_mensalidade=500,
            pl_observacao="",
        )

    class Meta:
        db_table = "plano"
        ordering = ["-id"]
        verbose_name = _("Plano")
        verbose_name_plural = _("Planos")


class Pagamento:
    class Meta:
        db_table = "pagamento"
        ordering = ["-id"]
        verbose_name = _("Pagamento")
        verbose_name_plural = _("Pagamentos")
