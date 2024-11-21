import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.system.base.models import Base


class Reserva:

    class Meta:
        db_table = "reserva"
        ordering = ["-id"]
        verbose_name = _("Reserva")
        verbose_name_plural = _("Reservas")
