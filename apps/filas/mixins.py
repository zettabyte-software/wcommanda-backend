import logging

from django.db.models.aggregates import Max
from django.utils.translation import gettext_lazy as _

from django_lifecycle import AFTER_CREATE, AFTER_SAVE, BEFORE_CREATE, hook

from lib.twilio.sms import TwilioSmsHandler

from .messages import MENSAGEM_ENTRADA_FILA_ESPERA

logger = logging.getLogger(__name__)


class FilaHooksMixin:
    @hook(BEFORE_CREATE)
    def setar_posicao_fila(self):
        if not self.ff_posicao:
            posicao_atual_fila = self.__class__.objects.aggregate(max=Max("ff_posicao"))["max"] or 0
            self.ff_posicao = posicao_atual_fila + 1
            logger.info("Setando posição %i", posicao_atual_fila)

    @hook(AFTER_CREATE)
    def enviar_sms_confirmacao(self):
        logger.info("Enviando sms de confirmação para")
        handler = TwilioSmsHandler()
        handler.enviar_sms(self.ff_telefone, MENSAGEM_ENTRADA_FILA_ESPERA)

    @hook(AFTER_SAVE)
    def enviar_sms_confirmacao_atualizacao(self):
        logger.info("Enviando sms de confirmação para")
        handler = TwilioSmsHandler()
        handler.enviar_sms(self.ff_telefone, MENSAGEM_ENTRADA_FILA_ESPERA)
