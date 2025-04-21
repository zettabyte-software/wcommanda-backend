import copy
import json

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.forms.models import model_to_dict
from django.utils.translation import gettext_lazy as _

from auditlog.models import AuditlogHistoryField
from django_lifecycle import LifecycleModel
from django_multitenant.fields import TenantForeignKey
from django_multitenant.models import TenantModel
from threadlocals.threadlocals import get_current_user


class Base(TenantModel, LifecycleModel):
    system_model = False

    tenant_id = "assinatura_id"

    ativo = models.BooleanField(_("ativo"), default=True)
    codigo = models.PositiveBigIntegerField(_("código"), editable=False, default=1)
    data_criacao = models.DateField(_("data de criação"), auto_now_add=True)
    hora_criacao = models.TimeField(_("hora de criação"), auto_now_add=True)
    data_ultima_alteracao = models.DateField(_("data da última alteração"), auto_now=True)
    hora_ultima_alteracao = models.TimeField(_("hora da última alteração"), auto_now=True)
    filial = TenantForeignKey(verbose_name=_("filial"), to="filiais.Filial", on_delete=models.PROTECT, null=True)
    owner = TenantForeignKey(verbose_name=_("owner"), to=settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True)
    assinatura = models.ForeignKey(verbose_name=_("tenant"), to="assinaturas.Assinatura", on_delete=models.PROTECT, null=True, blank=True)

    history = AuditlogHistoryField()

    all_objects = models.Manager()

    @property
    def json(self):
        data = model_to_dict(self)
        return json.dumps(data, default=str)

    def as_dict(self):
        data = model_to_dict(self)
        return data

    def clonar(self, commit=True, **fields):
        clone = copy.copy(self)
        for chave, valor in fields.items():
            setattr(clone, chave, valor)
        clone.save(commit=commit)
        return clone

    def save(self, *args, **kwargs):
        if not hasattr(self, "owner"):
            if self.system_model:
                user_cls = get_user_model()
                self.owner = user_cls.get_instacia_bot_wcommanda()
            else:
                self.owner = get_current_user()

        if self.pk is None:
            max_code = self.__class__.objects.all().aggregate(max=models.Max("codigo"))["max"] or 0
            self.codigo = max_code + 1

        return super().save(*args, **kwargs)

    @classmethod
    def get_column_names(cls):
        return [field.name for field in cls._meta.get_fields() if field.concrete and not field.is_relation]

    class Meta:
        abstract = True


class EstadosChoices(models.IntegerChoices):
    EM_BRANCO = 0, "Em branco"
    RONDONIA = 1, "Rondônia"
    ACRE = 2, "Acre"
    AMAZONAS = 3, "Amazonas"
    RORAIMA = 4, "Roraima"
    PARA = 5, "Pará"
    AMAPA = 6, "Amapá"
    TOCANTINS = 7, "Tocantins"
    MARANHAO = 8, "Maranhão"
    PIAUI = 9, "Piauí"
    CEARA = 10, "Ceará"
    RIO_GRANDE_DO_NORTE = 11, "Rio Grande do Norte"
    PARAIBA = 12, "Paraíba"
    PERNAMBUCO = 13, "Pernambuco"
    ALAGOAS = 14, "Alagoas"
    SERGIPE = 15, "Sergipe"
    BAHIA = 16, "Bahia"
    MINAS_GERAIS = 17, "Minas Gerais"
    ESPIRITO_SANTO = 18, "Espírito Santo"
    RIO_DE_JANEIRO = 19, "Rio de Janeiro"
    SAO_PAULO = 20, "São Paulo"
    PARANA = 21, "Paraná"
    SANTA_CATARINA = 22, "Santa Catarina"
    RIO_GRANDE_DO_SUL = 23, "Rio Grande do Sul"
    MATO_GROSSO_DO_SUL = 24, "Mato Grosso do Sul"
    MATO_GROSSO = 25, "Mato Grosso"
    GOIAS = 26, "Goiás"
    DISTRITO_FEDERAL = 27, "Distrito Federal"
    EXTERIOR = 28, "Exterior"
