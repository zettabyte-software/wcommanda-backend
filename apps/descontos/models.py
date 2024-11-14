import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from auditlog.registry import auditlog

from apps.system.base.models import Base


def gerar_codigo_cupon_aleatorio(*args):
    return str(uuid.uuid4())[:7].upper()


class TiposDescontoChoices(models.IntegerChoices):
    PORCENTUAL = 1, _("Porcentual")
    VALOR = 2, _("Valor")


class CuponDesconto(Base):
    cp_tipo = models.PositiveSmallIntegerField(_("tipo"), choices=TiposDescontoChoices.choices)
    cp_expiracao = models.DateField(_("expiração"), null=True)
    cp_valor = models.FloatField(_("valor"), default=0)
    cp_valor_minimo = models.IntegerField(_("valor mínimo"), default=0)
    cp_codigo = models.CharField(_("código"), max_length=10, default=gerar_codigo_cupon_aleatorio)
    cp_utilizado = models.BooleanField(_("utilizado"), default=False)

    def get_valor_com_desconto(self, valor):
        if self.cp_valor_minimo > valor:
            msg = "O valor %s não atende ao valor mínimo de %s" % (
                valor,
                self.cp_valor_minimo,
            )
            raise ValueError(msg)

        match self.cp_tipo:
            case TiposDescontoChoices.PORCENTUAL:
                valor_desconto = round((self.cp_valor / 100) * valor, 2)
                return valor - valor_desconto

            case TiposDescontoChoices.VALOR:
                return valor - self.cp_valor

    class Meta:
        db_table = "cupom_desconto"
        ordering = ["-id"]
        verbose_name = _("Cupon de Desconto")
        verbose_name_plural = _("Cupons de Desconto")


auditlog.register(CuponDesconto)
