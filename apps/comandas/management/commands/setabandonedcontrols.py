from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.comandas.models import Comanda, opcoes_status_comanda
from apps.system.core.classes import DatabasesLoader


class Command(BaseCommand):
    help = "Pega todas as comandas do sistemas que estão abertas e marca com 'ABANDONADA'. Executado todo dia 23h59."

    def handle(self, *args, **options):
        loader = DatabasesLoader()
        loader.carregar_banco_dados()
        for alias in settings.DATABASES:
            comandas_abandonadas = Comanda.objects.filter(
                cm_status=opcoes_status_comanda.ABERTA, data_criacao=timezone.now()
            ).using(alias)

            comandas_abandonadas.update(cm_status=opcoes_status_comanda.ABANDONADA)
