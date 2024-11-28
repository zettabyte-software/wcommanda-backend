from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.system.base.models import Base, EstadosChoices


class Cliente(Base):
    cl_nome = models.CharField(_("nome"), max_length=30)
    cl_sobrenome = models.CharField(_("nome"), max_length=50)
    cl_nascimento = models.DateField(_("data de nascimento"), null=True)

    # contato
    cl_celular = models.CharField(_("celular"), max_length=11, blank=True)
    cl_telefone = models.CharField(_("telefone"), max_length=10, blank=True)
    cl_email = models.EmailField(_("email"), blank=True)

    # endereço
    cl_cep = models.CharField(_("cep"), max_length=8, blank=True, default="")
    cl_estado = models.PositiveSmallIntegerField(_("estado"), choices=EstadosChoices.choices, default=EstadosChoices.EM_BRANCO)
    cl_cidade = models.CharField(_("cidade"), max_length=50, blank=True, default="")
    cl_bairro = models.CharField(_("bairro"), max_length=40, blank=True, default="")
    cl_rua = models.CharField(_("rua"), max_length=30, blank=True, default="")
    cl_numero = models.CharField(_("número"), max_length=8, blank=True, default="")
    cl_complemento = models.CharField(_("complemento"), max_length=100, blank=True, default="")

    class Meta:
        db_table = "cliente"
        ordering = ["-id"]
        verbose_name = _("Cliente")
        verbose_name_plural = _("Clientes")
