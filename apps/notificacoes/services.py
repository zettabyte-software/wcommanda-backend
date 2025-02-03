import logging

from apps.system.assinaturas.models import Assinatura
from apps.users.models import Usuario

from .models import Notificacao

logger = logging.getLogger(__name__)


def enviar_notificao_todos_os_usuarios(titulo: str, mensagem: str, assinatura: Assinatura | None = None):
    usuarios = Usuario.objects.none()
    if assinatura is None:
        usuarios = Usuario.all_objects.all()
    else:
        usuarios = Usuario.objects.all()

    notificacoes = []
    for usuario in usuarios:
        notificacao = Notificacao(
            nt_titulo=titulo,
            nt_mensagem=mensagem,
            nt_usuario=usuario,
        )
        notificacoes.append(notificacao)

    return Notificacao.objects.bulk_create(notificacoes)


def enviar_notificao_usuario(titulo: str, mensagem: str, usuario: Usuario):
    return Notificacao.objects.create(
        nt_titulo=titulo,
        nt_mensagem=mensagem,
        nt_usuario=usuario,
    )
