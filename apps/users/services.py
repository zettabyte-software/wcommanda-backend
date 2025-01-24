from threadlocals.threadlocals import get_request_variable

from apps.system.core.classes import Email
from apps.users.models import Usuario


def convidar_usuario_sistema(email: str):
    usuario = Usuario.objects.create(
        email=email,
        first_name="",
        last_name="",
        password="",
    )

    usuario.set_unusable_password()

    base_url = get_request_variable('host')
    token = get_request_variable("token")
    url = f"{base_url}auth/aceitar-convite?accessToken={token}&userId={usuario.pk}&email={email}"

    email_confirmacao = Email(
        titulo="Convite para o sistema",
        corpo=f"Olá! Você foi convidado para o wCommanda, para aceitar o convite, acesse o link: {url}",
        destinatarios=[email],
    )

    email_confirmacao.send()
