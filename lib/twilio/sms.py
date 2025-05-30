from django_multitenant.utils import get_current_tenant
from twilio.rest import Client

from apps.system.core.exceptions import WcommandaError
from utils.env import get_env_var


class SaldosInsuficientesError(WcommandaError):
    pass


class ClienteNaoTemPermissaoEnvioSmsError(WcommandaError):
    pass


class TwilioSmsHandler:
    SaldosInsuficientesError = SaldosInsuficientesError
    ClienteNaoTemPermissaoEnvioSmsError = ClienteNaoTemPermissaoEnvioSmsError

    def __init__(self):
        account_sid = get_env_var("TWILLIO_ACCOUNT_SID")
        auth_token = get_env_var("TWILLIO_AUTH_TOKEN")
        phone_number = get_env_var("TWILLIO_PHONE_NUMBER")

        self.phone_number = phone_number
        self.client = Client(account_sid, auth_token)

    def enviar_sms(self, numero: str, mensagem: str):
        self.validar_envio_sms()
        message = self.client.messages.create(
            to=f"+55{numero}",
            from_=self.phone_number,
            body=mensagem,
        )

        return message

    def validar_envio_sms(self):
        assinatura = get_current_tenant()
        plano = assinatura.ss_plano

        if not plano.pl_envia_sms:
            raise ClienteNaoTemPermissaoEnvioSmsError("Cliente não possui permissão para enviar SMS.")

        if plano.pl_saldo_sms == 0:
            raise self.SaldosInsuficientesError("Saldo insuficiente para enviar SMS.")
