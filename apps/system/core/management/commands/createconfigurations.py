from django.core.management.base import BaseCommand
from apps.system.core.records import DefaultRecordsManger

class Command(BaseCommand):
    help = 'Reseta o histórico de migrações do banco de dados do sistema'

    def handle(self, *args, **options):
        DefaultRecordsManger().apply_updates()
