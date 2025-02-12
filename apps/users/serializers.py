from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from rest_framework_simplejwt.serializers import PasswordField

from apps.filiais.models import Filial

from .models import StatusSolicitacaoChoices, Usuario
from .services import convidar_usuario_sistema


class UsuarioSerializer(serializers.ModelSerializer):
    password = PasswordField()

    def validate_password(self, password):
        validate_password(password)
        return make_password(password)

    class Meta:
        model = Usuario
        exclude = (
            "is_superuser",
            "groups",
            "user_permissions",
            "is_staff",
        )


class OnwerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
        )


class ConvidarUsuarioSerializer(serializers.Serializer):
    email = serializers.EmailField()
    filial = serializers.PrimaryKeyRelatedField(queryset=Filial.objects.all())

    def validate_email(self, value):
        email_ja_cadastrado = Usuario.all_objects.filter(email=value).exists()

        if email_ja_cadastrado:
            raise serializers.ValidationError({"email": _("Esse email já está cadastrado")})

        return value

    def save(self):
        email = self.validated_data["email"]  # type: ignore
        filial = self.validated_data["filial"]  # type: ignore
        convidar_usuario_sistema(email, filial)


class AceitarConviteSerializer(serializers.Serializer):
    email = serializers.SlugRelatedField(
        slug_field="email",
        queryset=Usuario.objects.filter(status=StatusSolicitacaoChoices.PENDENTE)
    )
    nome = serializers.CharField()
    sobrenome = serializers.CharField()
    senha = PasswordField()

    def save(self, **kwargs):
        usuario = self.validated_data["email"]  # type: ignore
        usuario.status = StatusSolicitacaoChoices.ACEITO
        usuario.first_name = self.validated_data["nome"]  # type: ignore
        usuario.last_name = self.validated_data["sobrenome"]  # type: ignore
        usuario.password = make_password(self.validated_data["senha"])  # type: ignore
        usuario.save()
