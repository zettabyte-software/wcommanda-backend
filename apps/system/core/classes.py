import json

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db import connection
from django.template.loader import get_template

from utils.env import get_env_var


class SingletonMeta(type):
    _instances = {}

    def __new__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__new__(cls, *args, **kwargs)
        return cls._instances[cls]


class DinamicAttrs:
    def __init__(self, dados):
        self.raw = dados
        for chave, valor in dados.items():
            if isinstance(valor, dict):
                valor = DinamicAttrs(valor)
            setattr(self, chave, valor)


class JSONDinamicAttrs(DinamicAttrs):
    def __init__(self, path):
        dados = json.loads(open(path).read())
        super().__init__(dados)


class CachedFile:
    __files = {}

    def __new__(cls, path, **kwargs):
        mode = kwargs.get("mode", "r")
        if cls.__files.get(path, None) is None:
            file = open(path, mode)
            cls.__files[path] = file

        return cls.__files[path]


class Email:
    MAX_RECIPIENTS = 200

    class InvalidRecipientsNumber(Exception):
        pass

    def __init__(self, titulo, corpo=None, destinatarios=[], from_email=settings.EMAIL_HOST_USER):
        self.titulo = titulo
        self.corpo = corpo

        self._destinatarios = destinatarios
        self._from_email = from_email

        self._template_path = None
        self._template = None

    def set_template(self, path, **context):
        self._template = get_template(path).render(context)

    def add_destinatario(self, destinatario):
        if destinatario in self._destinatarios:
            return

        if len(self._destinatarios) == self.MAX_RECIPIENTS:
            raise self.InvalidRecipientsNumber(f"O número máximo de destinatários é {self.MAX_RECIPIENTS}")

        self._destinatarios.append(destinatario)

    def send(self):
        if len(self._destinatarios) == 0:
            raise self.InvalidRecipientsNumber("Informe ao menos um destinatário")

        assert self.corpo is None or self._template_path is None, (
            "Os argumentos 'corpo' ou 'template' deve ser configurados"
        )

        email = EmailMultiAlternatives(
            subject=self.titulo,
            body=self.corpo or "",
            from_email=self._from_email,
            to=self._destinatarios,
        )

        if self._template is not None:
            email.attach_alternative(self._template, "text/html")

        email.send()


class DatabasesLoader:
    def __init__(self):
        self.bancos_dados = []

    def get_nomes_bancos_dados(self):
        self.cursor = connection.cursor()
        self.cursor.execute("SELECT datname FROM pg_database;")
        nomes = self.cursor.fetchall()
        self.bancos_dados = [nome[0] for nome in nomes if nome[0].startswith("wcommanda")]
        return self.bancos_dados

    def carregar_banco_dados(self):
        for db in self.bancos_dados:
            conf_db = {
                "ENGINE": "django.db.backends.postgresql",
                "NAME": db,
                "USER": get_env_var("DATABASE_USER"),
                "PASSWORD": get_env_var("DATABASE_PASSWORD"),
                "HOST": get_env_var("DATABASE_HOST"),
                "PORT": get_env_var("DATABASE_PORT"),
                "ATOMIC_REQUESTS": False,
                "AUTOCOMMIT": True,
                "CONN_MAX_AGE": 0,
                "CONN_HEALTH_CHECKS": False,
                "OPTIONS": {},
                "TIME_ZONE": None,
                "TEST": {
                    "CHARSET": None,
                    "COLLATION": None,
                    "MIGRATE": True,
                    "MIRROR": None,
                    "NAME": None,
                },
            }

            settings.DATABASES[db] = conf_db
