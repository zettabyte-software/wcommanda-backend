import logging

import httpx
import sentry_sdk

from apps.filiais.models import Filial
from apps.system.core.classes import DinamicAttrs

from ..dataclasses import EventoIfood
from ..limiter import LimitadorIntegracaoPedidosIfood
from ..models import PedidoIfood, PedidoItemComplementoIfood, PedidoItemIfood
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


class WebhookPedidoIfood(BaseIntegradorIfood):
    def criar_pedido_via_webhook(self, evento_ifood: dict) -> PedidoIfood | None:
        dados = EventoIfood(**evento_ifood)
        dados_pedido = self.get_dados_pedido(dados.orderId)

        if dados_pedido is None:
            return None

        pedido = self.criar_pedido(dados_pedido)
        self.criar_itens(pedido, dados_pedido.items)

        return pedido

    def get_dados_pedido(self, id_ifood: str) -> DinamicAttrs | None:
        try:
            response = self.client.get(f"order/v1.0/orders/{id_ifood}")
            response.raise_for_status()
            return DinamicAttrs(response.json())
        except (httpx.HTTPStatusError, httpx.DecodingError) as e:
            logger.error("Erro ao obter os dados do pedido no iFood: %s", e)
            sentry_sdk.capture_exception(e)
            return None

    def criar_pedido(self, dados_pedido: object):
        dados_endereco = dados_pedido.delivery.deliveryAddress

        limiter = LimitadorIntegracaoPedidosIfood()

        filial = Filial.objects.filter(fl_merchat_id_ifood=dados_pedido.merchant.id).first()

        pedido = PedidoIfood.objects.create(
            fd_ifood_id=dados_pedido.id,
            fd_teste=dados_pedido.isTest,
            fd_cep=dados_endereco.postalCode,
            fd_estado=dados_endereco.state,
            fd_cidade=dados_endereco.city,
            fd_bairro=dados_endereco.neighborhood,
            fd_rua=dados_endereco.streetName,
            fd_numero=dados_endereco.streetNumber,
            fd_complemento=dados_endereco.complement,
            filial=filial,
            ativo=limiter.atingiu_limite_pedidos,
        )

        return pedido

    def criar_itens(self, pedido: PedidoIfood, itens: list[dict]):
        for item_pedido in itens:
            item_pedido = DinamicAttrs(item_pedido)
            instance = PedidoItemIfood.objects.create(
                ft_pedido=pedido,
                ft_ifood_id=item_pedido.id,
                ft_index=item_pedido.index,
                ft_pedido_ifood=pedido.fd_ifood_id,
                ft_nome_produto=item_pedido.name,
                fd_imagem_produto=item_pedido.imageUrl,
                ft_unidade=item_pedido.unit,
                ft_preco_unitario=item_pedido.price,
                ft_quantidade=item_pedido.quantity,
                ft_preco_total=item_pedido.totalPrice,
                ft_observacao=item_pedido.observations,
                filial=pedido.filial,
            )

            if hasattr(item_pedido, "customizations"):
                self.criar_complementos(instance, item_pedido.customizations)

    def criar_complementos(self, item_pedido: PedidoItemIfood, customizacoes: list[dict]):
        for customizacao in customizacoes:
            dados = DinamicAttrs(customizacao)
            PedidoItemComplementoIfood.objects.create(
                pf_item_pedido=item_pedido,
                pf_ifood_id=dados.id,
                pf_nome=dados.name,
                pf_quantidade=dados.quantity,
                pf_tipo=dados.unitPrice,
                pf_preco_unitario=dados.unitPrice,
                pf_preco=dados.price,
            )


class IntegradorPedidosIfood(BaseIntegradorIfood):
    def confirmar(self, id: str):
        url = f"/order/v1.0/orders/{id}/confirm"
        response = self.client.post(url)
        logger.info(response.url)
        return response.status_code, response.text

    def iniciar_preparacao(self, id: str):
        url = f"/order/v1.0/orders/{id}/startPreparation"
        response = self.client.post(url)
        return response.status_code, response.text

    def preparar_recebimento(self, id: str):
        url = f"/order/v1.0/orders/{id}/readyToPickup"
        response = self.client.post(url)
        return response.status_code, response.text

    def dispachar(self, id: str):
        url = f"/order/v1.0/orders/{id}/dispatch"
        response = self.client.post(url)
        return response.status_code, response.text

    def solicitar_cancelamento(self, id: str, motivo_cancelamento: str):
        url = f"/order/v1.0/orders/{id}/requestCancellation"
        dados = {"reason": motivo_cancelamento, "cancellationCode": "501"}
        response = self.client.post(url, json=dados)
        return response.status_code, response.text
