from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from rest_framework_simplejwt.serializers import PasswordField

from .models import Usuario


class UsuarioSerializer(serializers.ModelSerializer):
    password = PasswordField()

    def validate_password(self, password):
        validate_password(password)

        if self.context.get("use_senha_integracao_field", False):
            return password
        else:
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
