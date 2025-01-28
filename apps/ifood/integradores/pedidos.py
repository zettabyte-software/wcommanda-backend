import logging

import httpx
import sentry_sdk

from apps.system.core.classes import DinamicAttrs

from ..dataclasses import EventoIfood
from ..limiter import LimitadorIntegracaoPedidosIfood
from ..models import PedidoIfood
from .base import BaseIntegradorIfood

""" TABELA DE TIPOS DE EVENTOS DO IFOOD
#################################################################################################################################
# EVENTO              CÓD.  DESCRIÇÃO                                                                                           #
#################################################################################################################################
# PLACED	          PLC   Novo pedido na plataforma                                                                           #
# CONFIRMED	          CFM   Pedido foi confirmado e será preparado                                                              #
# SEPARATION_STARTED  SPS   Indica o início do processo de separação dos itens do pedido (Exclusivo para pedidos de Mercado)    #
# SEPARATION_ENDED	  SPE   Indica a conclusão da sepração dos itens do pedido (Exclusivo para pedidos de Mercado)              #
# READY_TO_PICKUP	  RTP   Indica que o pedido está pronto para ser retirado (Pra Retirar)                                     #
# DISPATCHED          DSP   Indica que o pedido saiu para entrega (Delivery)                                                    #
# CONCLUDED      	  CON   Pedido foi concluído                                                                                #
# CANCELLED      	  CAN   Pedido foi cancelado                                                                                #
#################################################################################################################################
"""

logger = logging.getLogger(__name__)


class IntegradorPedidosIfood(BaseIntegradorIfood):
    def criar_pedido_via_webhook(self, evento_ifood: dict) -> PedidoIfood | None:
        dados = EventoIfood(**evento_ifood)
        dados_pedido = self.get_dados_pedido(dados.orderId)

        if dados_pedido is None:
            return None

        dados_endereco = dados_pedido.delivery.dadosAddress  # type: ignore

        limiter = LimitadorIntegracaoPedidosIfood()

        pedido = PedidoIfood.objects.create(
            fd_ifood_id=dados_pedido.id,  # type: ignore
            fd_teste=dados_pedido,
            fd_tipo_pedido=dados_pedido,
            fd_cep=dados_endereco.postalCode,
            fd_estado=dados_endereco.state,
            fd_cidade=dados_endereco.city,
            fd_bairro=dados_endereco.neighborhood,
            fd_rua=dados_endereco.streetName,
            fd_numero=dados_endereco.streetNumber,
            fd_complemento=dados_endereco.complement,
            ativo=limiter.atingiu_limite_pedidos
        )

        return pedido

    def get_dados_pedido(self, id_ifood: str) -> DinamicAttrs | None:
        try:
            response = self.client.get(f"order/v1.0/orders/{id_ifood}")
            response.raise_for_status()
            return DinamicAttrs(response.json())
        except (httpx.HTTPStatusError, httpx.DecodingError) as e:
            logger.error("Erro ao realizar login no iFood: %s", e)
            sentry_sdk.capture_exception(e)
            return None
