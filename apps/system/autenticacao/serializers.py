import uuid

from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import update_last_login
from django.contrib.auth.password_validation import validate_password
from django.core.cache import cache
from django.utils.module_loading import import_string
from django.utils.translation import gettext_lazy as _

from rest_framework import exceptions, serializers

from rest_framework_simplejwt.serializers import PasswordField, TokenObtainPairSerializer

from apps.system.core.classes import Email
from apps.users.models import Usuario

REDEFINIR_SENHA_CACHE_KEY = "reset-password-%s"

CONFIRMAR_EMAIL_CACHE_KEY = "email-confirm-%s"


class LoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        authenticate_kwargs = {
            self.username_field: attrs[self.username_field],
            "password": attrs["password"],
        }

        try:
            authenticate_kwargs["request"] = self.context["request"]
        except KeyError:
            pass

        usuario = Usuario.objects.filter(email=authenticate_kwargs[self.username_field]).first()

        if not usuario:
            raise exceptions.AuthenticationFailed(
                {"mensagem": _("Esse email não está cadastrado em nossa base de dados")},
                "not_found_account",
            )

        if not usuario.is_active:
            raise exceptions.AuthenticationFailed(
                {"mensagem": _("O seu usuário foi inativado")},
                "inactive_account",
            )

        self.user = authenticate(**authenticate_kwargs)

        authentication_rule = import_string(settings.SIMPLE_JWT["USER_AUTHENTICATION_RULE"])

        if not authentication_rule(self.user):
            raise exceptions.AuthenticationFailed(
                {"mensagem": _("A senha informada está incorreta")},
                "incorret_password",
            )

        data = {}
        token = self.get_token(self.user, self.context["host"])
        data["access"] = str(token.access_token)  # type: ignore

        if settings.SIMPLE_JWT["UPDATE_LAST_LOGIN"]:
            update_last_login(None, self.user)  # type: ignore

        return data

    @classmethod
    def get_token(cls, user, aud):
        token = super().get_token(user)
        token["aud"] = aud
        token["user_name"] = user.first_name
        token["user_last_name"] = user.last_name
        token["user_full_name"] = user.get_full_name()
        token["user_enviroment"] = user.assinatura.pk
        token["branch"] = user.filial.pk
        return token


class EnviarEmailRedefinicaoSenhaSerializer(serializers.Serializer):
    usuario = serializers.SlugRelatedField(
        queryset=Usuario.objects.all(),
        slug_field="email",
    )

    def save(self):
        usuario = self.validated_data["usuario"]  # type: ignore

        cache_key = REDEFINIR_SENHA_CACHE_KEY % usuario.email

        codigo = uuid.uuid4().hex[:8].upper()
        cache.set(cache_key, codigo, 60 * 10)

        email = Email(
            titulo="Redefinição de senha",
            corpo=f"Esse é o código da redefinição de senha: {codigo}",
            destinatarios=[usuario.email],
        )

        email.send()


class RedefinirSenhaSerializer(serializers.Serializer):
    usuario = serializers.SlugRelatedField(queryset=Usuario.objects.all(), slug_field="email")
    nova_senha = serializers.CharField()
    codigo = serializers.CharField()

    def validate_nova_senha(self, value):
        validate_password(value)
        return value

    def validate(self, attrs):
        dados = super().validate(attrs)

        codigo = dados["codigo"]
        usuario = dados["usuario"]

        cache_key = REDEFINIR_SENHA_CACHE_KEY % usuario.email
        codigo_cache = cache.get(cache_key, None)

        if codigo_cache is None:
            raise serializers.ValidationError(
                {"mensagem": _("A redefinição de senha expirou. Solicite uma nova para redefinir sua senha")}
            )

        if codigo != codigo_cache:
            raise serializers.ValidationError({"mensagem": _("O código informado é inválido")})

        cache.delete(cache_key)

        return dados

    def save(self):
        nova_senha = self.validated_data["nova_senha"]  # type: ignore
        usuario = self.validated_data["usuario"]  # type: ignore

        usuario.password = make_password(nova_senha)
        usuario.save()


class TrocarSenhaSerializer(serializers.Serializer):
    usuario = serializers.PrimaryKeyRelatedField(queryset=Usuario.objects.all())
    senha_atual = PasswordField()
    nova_senha = PasswordField()

    def validate_nova_senha(self, senha):
        validate_password(senha)
        return make_password(senha)

    def validate(self, attrs):
        dados = super().validate(attrs)

        errors = {}
        senha_atual = dados["senha_atual"]
        usuario = dados["usuario"]

        if not usuario.check_password(senha_atual):
            errors["senha_atual"] = "A senha informada está incorreta"

        if errors.keys():
            raise serializers.ValidationError(errors)

        return dados

    def save(self):
        usuario = self.validated_data["usuario"]  # type: ignore
        nova_senha = self.validated_data["nova_senha"]  # type: ignore
        usuario.set_password(nova_senha)
        return usuario
