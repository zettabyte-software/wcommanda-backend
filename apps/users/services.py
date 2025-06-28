from threadlocals.threadlocals import get_request_variable

from apps.filiais.models import Filial
from apps.system.core.classes import Email
from apps.users.models import Usuario


def convidar_usuario_sistema(email: str, filial: Filial):
    usuario = Usuario.objects.create(
        email=email,
        filial=filial,
        first_name="",
        last_name="",
        password="",
    )

    usuario.set_unusable_password()

    base_url = get_request_variable('host')
    token = get_request_variable("token") # TODO rever isso
    url = f"https://{base_url}/cadastro?accessToken={token}&userId={usuario.pk}&email={email}"

    email_confirmacao = Email(
        titulo="Convite para o sistema",
        corpo=f"Olá! Você foi convidado para o wCommanda, para aceitar o convite, acesse o link: {url}",
        destinatarios=[email],
    )

    email_confirmacao.send()
