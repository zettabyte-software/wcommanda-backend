import random

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

from auditlog.registry import auditlog
from django_multitenant.models import TenantManager

from apps.system.base.models import Base


class StatusSolicitacao(models.IntegerChoices):
    PENDENTE = 1, _("Pendente")
    ACEITO = 2, _("Aceito")
    RECUSADO = 3, _("Recusado")


class UsuarioManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class MultitenantUsuarioManager(UsuarioManager, TenantManager):
    pass


class Usuario(Base, AbstractUser):
    username = None
    ativo = None
    owner = None

    WCOMMANDA_USER_EMAIL = "bot@wcommanda.com.br"

    status = models.PositiveSmallIntegerField(_("status"), choices=StatusSolicitacao.choices, default=StatusSolicitacao.PENDENTE)
    first_name = models.CharField(_("nome"), max_length=30)
    last_name = models.CharField(_("sobrenome"), max_length=60)
    email = models.EmailField(_("email"), unique=True)
    is_waiter = models.BooleanField(_("é garçom"), default=False)
    is_screen = models.BooleanField(_("é usuário tela"), default=False)

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = MultitenantUsuarioManager()
    all_objects = UsuarioManager()

    @staticmethod
    def get_instacia_bot_wcommanda():
        bot, _ = Usuario.objects.get_or_create(
            email=Usuario.WCOMMANDA_USER_EMAIL,
            defaults={
                "first_name": "Bot",
                "last_name": "wCommanda",
                "email": Usuario.WCOMMANDA_USER_EMAIL,
                "password": make_password(str(random.randint(10000, 100000))),
            },
        )

        return bot

    @staticmethod
    def get_id_bot_wcommanda():
        return Usuario.get_instacia_bot_wcommanda().pk

    def __str__(self) -> str:
        return self.email

    class Meta:
        db_table = "usuario"
        ordering = ["-id"]
        verbose_name = _("Usuário")
        verbose_name_plural = _("Usuários")


auditlog.register(
    Usuario,
    exclude_fields=[
        "last_login",
        "data_ultima_alteracao",
        "hora_ultima_alteracao",
    ],
)
