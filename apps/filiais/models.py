import random

from django.db import models
from django.utils.translation import gettext_lazy as _

from django_multitenant.utils import get_current_tenant

from apps.system.base.models import Base, EstadosChoices


class Filial(Base):
    filial = None

    fl_nome = models.CharField(_("nome"), max_length=120)

    fl_cep = models.CharField(_("cep"), max_length=8, blank=True, default="")
    fl_estado = models.PositiveSmallIntegerField(
        _("estado"),
        choices=EstadosChoices.choices,
        default=EstadosChoices.EM_BRANCO,
    )
    fl_cidade = models.CharField(_("cidade"), max_length=50, blank=True, default="")
    fl_bairro = models.CharField(_("bairro"), max_length=40, blank=True, default="")
    fl_rua = models.CharField(_("rua"), max_length=30, blank=True, default="")
    fl_numero = models.CharField(_("número"), max_length=8, blank=True, default="")
    fl_complemento = models.CharField(_("complemento"), max_length=100, blank=True, default="")

    fl_celular = models.CharField(_("celular"), max_length=11, blank=True)
    fl_telefone = models.CharField(_("telefone"), max_length=10, blank=True)
    fl_email = models.EmailField(_("email"), blank=True)

    fl_merchat_id_ifood = models.UUIDField(_("id do merchant do iFood"), null=True, default=None)
    fl_catalog_id = models.UUIDField(_("id do catálogo digital do iFood"), null=True, default=None)
    fl_delivery_catalog_id = models.UUIDField(_("id do catálogo de delivery do iFood"), null=True, default=None)

    def make_upload_path(self, filename):
        file_extension = filename.split(".")[-1]
        new_file_name = random.randint(1000000, 9999999)
        tenant = get_current_tenant()
        return f"{tenant.pk}//filiais/{new_file_name}.{file_extension}"

    fl_logo = models.ImageField(_("logo"), upload_to=make_upload_path, blank=True, null=True)

    class Meta:
        db_table = "filial"
        ordering = ["-id"]
        verbose_name = _("Filial")
        verbose_name_plural = _("Filiais")
