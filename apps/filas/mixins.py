import logging

from django.conf import settings
from django.db.models.aggregates import Max

from django_lifecycle import AFTER_CREATE, BEFORE_CREATE, hook
from threadlocals.threadlocals import get_current_request

from lib.twilio.sms import TwilioSmsHandler

from .messages import MENSAGEM_ENTRADA_FILA_ESPERA

logger = logging.getLogger(__name__)


class FilaHooksMixin:
    @hook(BEFORE_CREATE)
    def setar_posicao_fila(self):
        posicao_atual_fila = self.__class__.objects.aggregate(max=Max("ff_posicao"))["max"] or 0
        self.ff_posicao = posicao_atual_fila + 1
        logger.info("Setando posição %i", posicao_atual_fila)

    @hook(AFTER_CREATE)
    def enviar_sms_confirmacao(self):
        if not settings.IN_PRODUCTION:
            return

        request = get_current_request()
        host = request.headers.get(settings.TENANT_HOST_HEADER)
        link = f"https://{host}/espaco-do-cliente/fila-de-espera/{self.ff_uuid}/"
        mensagem = MENSAGEM_ENTRADA_FILA_ESPERA % link

        logger.info("Enviando sms de confirmação para")

        handler = TwilioSmsHandler()
        handler.enviar_sms(self.ff_celular, mensagem)
