from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.system.base.models import Base


class Fila(Base):
    ff_posicao = models.PositiveSmallIntegerField(_("posição"), default=1)
    ff_cliente = models.CharField(_("cliente"), max_length=40)
    ff_telefone = models.CharField(_("cliente"), max_length=11)
    ff_observacao = models.CharField(_("cliente"), max_length=60)

    class Meta:
        db_table = "fila"
        ordering = ["-id"]
        verbose_name = _("Fila")
        verbose_name_plural = _("Filas")

    @classmethod
    def remover_pessoa(cls, fila_id):
        pesosa = cls.objects.filter(id=fila_id).first()
        if not pesosa:
            raise ValueError(_("Pessoa não encontrada"))

        pesosa.delete()

        pessoas_restantes = cls.objects.all().order_by("ff_posicao")
        for index, fila in enumerate(pessoas_restantes, start=1):
            fila.ff_posicao = index
            fila.save()

    @classmethod
    def mudar_posicao(cls, fila_id, nova_posicao):
        pessoa = cls.objects.filter(id=fila_id).first()

        if not pessoa:
            raise ValueError(_("Pessoa não encontrada"))

        total_pessoas = cls.objects.count()
        if nova_posicao < 1 or nova_posicao > total_pessoas:
            raise ValueError(_("Nova posição fora do intervalo permitido."))

        posicao_antiga = pessoa.ff_posicao

        if posicao_antiga == nova_posicao:
            return

        if posicao_antiga < nova_posicao:
            filas_a_mover = cls.objects.filter(ff_posicao__gt=posicao_antiga, ff_posicao__lte=nova_posicao)
            for fila in filas_a_mover:
                fila.ff_posicao -= 1
                fila.save()
        else:
            filas_a_mover = cls.objects.filter(ff_posicao__gte=nova_posicao, ff_posicao__lt=posicao_antiga)
            for fila in filas_a_mover:
                fila.ff_posicao += 1
                fila.save()

        pessoa.ff_posicao = nova_posicao
        pessoa.save()
