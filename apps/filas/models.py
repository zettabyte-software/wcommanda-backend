from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.system.base.models import Base


class Fila(Base):
    ff_posicao = models.PositiveSmallIntegerField(_("posição"), default=1)
    ff_cliente = models.CharField(_("cliente"), max_length=40)
    ff_telefone = models.CharField(_("telefone"), max_length=11)
    ff_observacao = models.CharField(_("observação"), max_length=60, blank=True, default="")

    @classmethod
    def receber_pessoas(cls, *posicoes):
        if not posicoes:
            posicoes = (1,)

        pessoas_removidas = cls.objects.filter(ff_posicao__in=posicoes).order_by("ff_posicao")
        if not pessoas_removidas.exists():
            raise ValueError(_("Nenhuma pessoa encontrada nas posições especificadas."))

        pessoas_removidas.delete()

        filas_restantes = cls.objects.all().order_by("ff_posicao")
        for index, fila in enumerate(filas_restantes, start=1):
            fila.ff_posicao = index
            fila.save()

    @classmethod
    def remover_pessoa(cls, fila_id: int):
        pesosa = cls.objects.filter(id=fila_id).first()
        if not pesosa:
            raise ValueError(_("Pessoa não encontrada"))

        pesosa.delete()

        pessoas_restantes = cls.objects.all().order_by("ff_posicao")
        for index, fila in enumerate(pessoas_restantes, start=1):
            fila.ff_posicao = index
            fila.save()

    @classmethod
    def mudar_posicao(cls, fila_id: int, nova_posicao: int):
        posicao_fila = cls.objects.filter(id=fila_id).first()

        if not posicao_fila:
            raise ValueError(_("Pessoa não encontrada"))

        total_pessoas = cls.objects.count()
        if nova_posicao < 1 or nova_posicao > total_pessoas:
            raise ValueError(_("Nova posição fora do intervalo permitido."))

        posicao_antiga = posicao_fila.ff_posicao

        if posicao_antiga == nova_posicao:
            raise ValueError(_("As posições não podem ser as mesmas"))

        # avançando posições na fila
        if nova_posicao > posicao_antiga:
            pessoas_fila = cls.objects.filter(ff_posicao__gt=posicao_antiga, ff_posicao__lte=nova_posicao).exclude(id=fila_id)
            for pessoa in pessoas_fila:
                pessoa.ff_posicao -= 1
                pessoa.save()

        # voltando posições na fila
        else:
            pessoas_fila = cls.objects.filter(ff_posicao__gte=nova_posicao, ff_posicao__lt=posicao_antiga).exclude(id=fila_id)
            for pessoa in pessoas_fila:
                pessoa.ff_posicao += 1
                pessoa.save()

        posicao_fila.ff_posicao = nova_posicao
        posicao_fila.save()

    class Meta:
        db_table = "fila"
        ordering = ["-id"]
        verbose_name = _("Fila")
        verbose_name_plural = _("Filas")
