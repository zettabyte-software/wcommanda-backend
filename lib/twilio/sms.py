from twilio.rest import Client

from utils.env import get_env_var


class TwilioSmsHandler:
    def __init__(self):
        account_sid = get_env_var("TWILLIO_ACCOUNT_SID")
        auth_token = get_env_var("TWILLIO_AUTH_TOKEN")

        self.phone_number = get_env_var("TWILLIO_PHONE_NUMBER")
        self.client = Client(account_sid, auth_token)

    def enviar_sms(self, numero: str, mensagem: str):
        message = self.client.messages.create(
            to=f"+{numero}", # 5531975194725, +5531995773311
            from_=self.phone_number,
            body=mensagem,
        )

        return message
