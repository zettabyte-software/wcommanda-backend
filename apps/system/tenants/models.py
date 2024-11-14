from django.db import models
from django.utils.translation import gettext_lazy as _

from django_multitenant.models import TenantModel


class Ambiente(TenantModel):
    tenant_id = "id"

    mb_subdominio = models.CharField(_("subdomínio"), max_length=30, unique=True)
    mb_nome = models.CharField(_("nome"), max_length=100)

    def __str__(self):
        return self.mb_nome

    class Meta:
        db_table = "ambiente"
        ordering = ["-id"]
        verbose_name = _("Ambiente")
        verbose_name_plural = _("Ambientes")
