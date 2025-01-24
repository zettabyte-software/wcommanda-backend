from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from rest_framework_simplejwt.views import TokenObtainPairView

from apps.system.base.views import BaseViewSet
from apps.users.serializers import UsuarioSerializer

from .serializers import (
    EnviarEmailRedefinicaoSenhaSerializer,
    RedefinirSenhaSerializer,
    TrocarSenhaSerializer,
    Usuario,
)


class LoginViewSet(TokenObtainPairView):
    authentication_classes = []
    permission_classes = [AllowAny]


class CadastroViewSet(BaseViewSet):
    serializer_class = UsuarioSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AuthViewSet(BaseViewSet):
    serializer_class = UsuarioSerializer
    authentication_classes = []
    permission_classes = [AllowAny]
    serializer_classes = {
        "cadastro": UsuarioSerializer,
        "enviar_email_redefinicao_senha": EnviarEmailRedefinicaoSenhaSerializer,
        "redefinir_senha": RedefinirSenhaSerializer,
        "trocar_senha": TrocarSenhaSerializer,
    }

    @action(methods=["get"], detail=False)
    def validar_cadastro_email(self, request):
        email = request.query_params.get("email", None)
        if email is None:
            raise ValidationError({"email": "Essa query é obrigatória"})

        email_cadastrado = Usuario.objects.filter(email=email).exists()
        return Response({"cadastrado": email_cadastrado})

    @action(methods=["post"], detail=False)
    def enviar_email_redefinicao_senha(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response()

    @action(methods=["post"], detail=False)
    def redefinir_senha(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response()

    @action(methods=["post"], detail=False)
    def trocar_senha(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response()
