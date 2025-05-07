from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.system.base.models import Base


class Upload(Base):
    ld_content_type = models.ForeignKey(_("content type"), "contenttypes.ContentType", on_delete=models.PROTECT)
    ld_registro_id = models.PositiveBigIntegerField(_("id do registro"))
    ld_registro = GenericForeignKey("ld_content_type", "ld_registro_id")
    ld_back_blaze_id = models.CharField(_("id do upload no back blaze"), max_length=256)
    ld_back_blaze_path = models.CharField(_("path do bucket back blaze"), max_length=256)
    ld_back_blaze_url = models.CharField(_("url amigável back blaze"), max_length=256)

    class Meta:
        db_table = "upload"
        ordering = ["-id"]
        verbose_name = _("Upload")
        verbose_name_plural = _("Uploads")
