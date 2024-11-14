from django.utils.translation import gettext_lazy as _

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.system.base.views import BaseModelViewSet
from utils.rabbitmq import Publisher

from .serializers import Usuario, UsuarioSerializer


class UsuarioViewSet(BaseModelViewSet):
    model = Usuario
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    filterset_fields = {
        "email": ["exact"],
        "is_waiter": ["exact"],
    }

    @action(methods=["get"], detail=False)
    def verificar_cadastro_email(self, request):
        email_usuario = self.request.query_params.get("email", None)
        if email_usuario is None:
            raise ValidationError({"mensagem": "A query 'email' é obrigatória"})
        try:
            Usuario.objects.get(email=email_usuario)
            return Response()
        except Usuario.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @action(methods=["post"], detail=True)
    def ativar_usuario(self, request, pk):
        usuario = self.get_object()
        usuario.is_active = True
        usuario.save()
        subdominio = self.get_subdominio()
        publisher = Publisher("ativar-inativar-usuario-1.0.0")
        dados = {
            "email": usuario.email,
            "subdominio": subdominio,
            "sistema": 1,
            "ativo": True,
        }
        publisher.publish(dados)
        return Response({"mensagem": _("Usuário ativado")})

    @action(methods=["post"], detail=True)
    def inativar_usuario(self, request, pk):
        usuario = self.get_object()
        usuario.is_active = True
        usuario.save()
        subdominio = self.get_subdominio()
        publisher = Publisher("ativar-inativar-usuario-1.0.0")
        dados = {
            "email": usuario.email,
            "subdominio": subdominio,
            "sistema": 1,
            "ativo": False,
        }
        publisher.publish(dados)
        return Response({"mensagem": _("Usuário inativado")})


class CadastroViewSet(GenericViewSet, CreateModelMixin):
    serializer_class = UsuarioSerializer
    authentication_classes = []
    permission_classes = [AllowAny]

    def get_serializer(self, **kwargs):
        return UsuarioSerializer(**kwargs)
