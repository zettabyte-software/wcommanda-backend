from .models import Usuario


def get_usuario_wcommanda():
    return Usuario.objects.get(email=Usuario.WCOMMANDA_USER_EMAIL)
