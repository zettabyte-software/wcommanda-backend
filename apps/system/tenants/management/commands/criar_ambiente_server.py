import json
import logging

from django.core.management.base import BaseCommand
from django.db import transaction

import dotenv

from apps.system.conf.models import Configuracao
from apps.system.tenants.models import Ambiente
from apps.users.models import Usuario
from utils.rabbitmq import Consumer

logger = logging.getLogger("api")


class Command(BaseCommand):
    help = "Cria um ambiente para o wcommanda"

    def handle(self, *args, **options):
        consumer = Consumer("criar-ambiente-1.0.0", callback)
        try:
            dotenv.load_dotenv('.env')
            print("Iniciando servidor AMQP...")
            consumer.start_server()
        except KeyboardInterrupt:
            print("Encerrando servidor AMQP")
        finally:
            consumer.close_connection()


@transaction.atomic
def callback(ch, method, properties, body):
    print("Mensagem recebida")

    dados = Consumer.byte2dict(body)
    print(dados)

    with transaction.atomic():
        pid = transaction.savepoint()
        try:
            dados_ambiente = dados["ambiente"]
            ambiente = Ambiente.objects.create(
                mb_nome=dados_ambiente["mb_nome"],
                mb_subdominio=dados_ambiente["mb_subdominio"],
            )

            print("Ambiente %s criada com sucesso", dados_ambiente["mb_nome"])

            dados_usuario = dados["usuario"]
            usuario, _ = Usuario.objects.get_or_create(
                email=dados_usuario["email"],
                defaults={
                    "ambiente": ambiente,
                    "email": dados_usuario["email"],
                    "first_name": dados_usuario["first_name"],
                    "last_name": dados_usuario["last_name"],
                    "password": dados_usuario["password"],
                    "is_superuser": False,
                    "is_staff": False,
                },
            )

            print("Usuário %s integrado com sucesso", usuario.email)

            criar_configuracoes(ambiente)

        except Exception as exc:
            print(exc)
            raise exc from exc
            print("Erro ao criar ambiente")
            transaction.savepoint_rollback(pid)
            ch.basic_ack(delivery_tag=method.delivery_tag)


def criar_configuracoes(ambiente: Ambiente):
    arquivo = open("data/records/default/configuracoes.json")
    configuracoes = json.loads(arquivo.read())  # noqa: W291

    data = []
    for configuracao in configuracoes:
        dados = configuracao["data"]
        dados["ambiente"] = ambiente
        conf = Configuracao(**dados)
        data.append(conf)

    instances = Configuracao.objects.bulk_create(data)

    print("Configurações criadas com sucesso")

    return instances
