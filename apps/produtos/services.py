from django.db.models import Max

from .models import Produto


def sugerir_novo_codigo_cardapio():
    codigo = Produto.objects.aggregate(codigo=Max("pr_codigo_cardapio"))["codigo"] or 0
    return int(codigo) + 1
