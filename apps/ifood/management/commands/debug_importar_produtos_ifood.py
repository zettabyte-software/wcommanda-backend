import logging

from django.core.management.base import BaseCommand

from apps.ifood.integradores.produtos import ImportadorProdutosIfood

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Debuga o processo de importação de produtos do iFood"

    def handle(self, *args, **options):
        DEBUG_MERCHANT = "85330304-7ee6-4182-b40d-6c65cca35a65"
        integrador = ImportadorProdutosIfood(DEBUG_MERCHANT)
        integrador.importar_produtos()
        logger.info("Produtos integrados com sucesso!")
