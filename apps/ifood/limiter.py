import logging

from django_multitenant.utils import get_current_tenant

from apps.ifood.models import PedidoIfood
from utils.date import gerar_primeiro_e_ultimo_dia_mes

logger = logging.getLogger(__name__)


class LimitadorIntegracaoPedidosIfood:
    def __init__(self):
        tenant = get_current_tenant()
        self.tenant = tenant
        self.limite = 5  # tenant.ss_plano.pl_numero_integracoes_ifood  # type: ignore

    @property
    def total_pedidos_mes(self):
        range_mes = gerar_primeiro_e_ultimo_dia_mes()
        total_pedidos = PedidoIfood.objects.filter(data_criacao__range=range_mes).count()
        return total_pedidos

    @property
    def atingiu_limite_pedidos(self):
        logger.info("Atingiu o limite: %s > %s (%s)", self.total_pedidos_mes, self.limite, self.total_pedidos_mes >= self.limite)
        return self.total_pedidos_mes > self.limite
