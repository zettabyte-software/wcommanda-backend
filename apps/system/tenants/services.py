from django.conf import settings
from django.core.management import call_command
from django.contrib.auth.hashers import make_password
from django.db import connection, connections

from threadlocals.threadlocals import get_current_request

from utils.jwt import decode_jwt

from apps.system.core.records import DefaultRecordsManger
from apps.system.core.classes import Email

from apps.users.models import Usuario


class TenantManager:
    def __init__(self, dados):
        self.dados = dados
        self.cursor = connection.cursor()

    def criar_tenant(self):
        self.criar_banco_dados()
        self.alterar_conexao_db()
        self.migrar_banco_dados()
        self.criar_usuario_wcommanda()
        self.criar_usuario_root()
        self.popular_registros_padroes()
        self.reiniciar_conexao_db()
        self.enviar_email_boas_vindas()

    def criar_banco_dados(self):
        self.cursor.execute(f"CREATE DATABASE {self.dados['nome_banco_dados']};")

    def criar_usuario_wcommanda(self):
        usuario = Usuario()
        usuario.first_name = "Bot"
        usuario.last_name = "wCommanda"
        usuario.email = "bot@wcommanda.com.br"
        usuario.password = make_password("StrongPassword!987654321")
        usuario.save()

    def criar_usuario_root(self):
        usuario = Usuario()
        usuario.first_name = self.dados["nome_usuario"]
        usuario.last_name = self.dados["sobrenome_usuario"]
        usuario.email = self.dados["email_usuario"]
        usuario.password = make_password(self.dados["senha_usuario"])
        usuario.save()

    def migrar_banco_dados(self):
        call_command("migrate")

    def popular_registros_padroes(self):
        manager = DefaultRecordsManger()
        manager.populate()

    def alterar_conexao_db(self):
        connection.close()
        settings.DATABASES["default"]["NAME"] = self.dados["nome_banco_dados"]
        connections["default"].close()
        connection.ensure_connection()

    def reiniciar_conexao_db(self):
        connection.close()
        settings.DATABASES["default"]["NAME"] = "wcommanda"
        connections["default"].close()
        connection.ensure_connection()

    def enviar_email_boas_vindas(self):
        link = ""
        email = Email(
            titulo="Boas vindas ao wCommanda!",
            corpo=f"Seja bem vindo ao sistema! Confirme seu email clicando no link abaixo: \n {link}",
        )


def get_current_tenant():
    request = get_current_request()
    token = request.headers["Authorization"].split(" ")[1]
    payload = decode_jwt(token)
    return payload["user_tenant"]


def get_current_token():
    request = get_current_request()
    token = request.headers["Authorization"].split(" ")[1]
    return token
