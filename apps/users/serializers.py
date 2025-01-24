from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers

from rest_framework_simplejwt.serializers import PasswordField

from .models import Usuario
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

    def validate_email(self, value):
        email_ja_cadastrado = Usuario.all_objects.filter(email=value).exists()
        if email_ja_cadastrado:
            raise serializers.ValidationError({"email": _("Esse email já está cadastrado")})
        return value

    def save(self):
        convidar_usuario_sistema(self.validated_data["email"])  # type: ignore
