from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from django_multitenant.fields import TenantForeignKey

from apps.system.base.models import Base


class Notificacao(Base):
    system_model = True

    nt_titulo = models.CharField(_("título"), max_length=80)
    nt_mensagem = models.CharField(_("mensagem"), max_length=80)
    nt_usuario = TenantForeignKey(
        verbose_name=_("usuário"),
        to=settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        null=True,
        default=None,
        related_name="usuarios"
    )
    nd_lida = models.BooleanField(_("lida"))

    class Meta:
        db_table = "notificacao"
        ordering = ["-id"]
        verbose_name = _("Notificação")
        verbose_name_plural = _("Notificações")
