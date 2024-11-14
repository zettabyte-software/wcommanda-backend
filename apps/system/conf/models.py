from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.system.base.models import Base

from .types import TCodigoConfiguracao


class Configuracao(Base):
    owner = None

    class opcoes_configuracoes:
        WCM_CONTROLE_STATUS_ITENS = "WCM_CONTROLE_STATUS_ITENS"
        WCM_REINICIO_CODIGO_COMANDA = "WCM_REINICIO_CODIGO_COMANDA"
        WCM_CONTROLE_ESTOQUE = "WCM_CONTROLE_ESTOQUE"
        WCM_PERCENTUAL_COMISSAO_GARCON = "WCM_PERCENTUAL_COMISSAO_GARCON"
        WCM_CLIENT_ID_IFOOD = "WCM_CLIENT_ID_IFOOD"
        WCM_CLIENT_SECRET_IFOOD = "WCM_CLIENT_SECRET_IFOOD"

    primitive_types_codes_map = {
        "WCM_CONTROLE_STATUS_ITENS": bool,
        "WCM_REINICIO_CODIGO_COMANDA": bool,
        "WCM_CONTROLE_ESTOQUE": bool,
        "WCM_PERCENTUAL_COMISSAO_GARCON": float,
        "WCM_CLIENT_ID_IFOOD": float,
        "WCM_CLIENT_SECRET_IFOOD": float,
    }

    cf_codigo = models.CharField(_("código"), max_length=40, editable=False)
    cf_descricao = models.CharField(_("descrição"), max_length=100)
    cf_valor = models.CharField(_("valor"), max_length=25)

    @classmethod
    def normalize_value(cls, codigo, valor):
        tipo_valor_parametro = cls.primitive_types_codes_map[codigo]

        if tipo_valor_parametro is str:
            return valor

        if tipo_valor_parametro is int:
            return int(valor)

        if tipo_valor_parametro is float:
            return float(valor)

        if tipo_valor_parametro is bool:
            return True if valor == "True" else False

        raise ImproperlyConfigured(f"Tipo de valor não suportado para o código de configuração {codigo}")

    @classmethod
    def get_configuracao(cls, codigo: TCodigoConfiguracao):
        param = cls.objects.get(cf_codigo=codigo)
        return cls.normalize_value(codigo, param.cf_valor)

    class Meta:
        db_table = "configuracao"
        ordering = ["-id"]
        verbose_name = _("Configuração")
        verbose_name_plural = _("Configurações")

    def __str__(self):
        return self.cf_codigo


configuracoes = Configuracao.opcoes_configuracoes
