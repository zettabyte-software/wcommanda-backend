import logging

from django.db.models import IntegerField, Max
from django.db.models.functions import Cast

from .models import Produto

logger = logging.getLogger(__name__)


def gerar_codigo_cardapio():
    codigo = (
        Produto.objects.annotate(codigo_num=Cast("pr_codigo_cardapio", IntegerField())).aggregate(
            codigo=Max("codigo_num")
        )["codigo"]
        or 0
    )
    return int(codigo) + 1
