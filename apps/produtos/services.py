from django.db.models import Max

from .models import Produto


def gerar_codigo_cardapio():
    codigo = Produto.objects.aggregate(codigo=Max("pr_codigo_cardapio"))["codigo"] or 0
    return int(codigo) + 1
