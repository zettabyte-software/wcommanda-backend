from django.utils.translation import gettext_lazy as _

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from apps.system.base.views import BaseModelViewSet

from .serializers import ConvidarUsuarioSerializer, Usuario, UsuarioSerializer


class UsuarioViewSet(BaseModelViewSet):
    model = Usuario
    queryset = Usuario.objects.all()
    serializer_classes = {
        "list": UsuarioSerializer,
        "retrieve": UsuarioSerializer,
        "create": UsuarioSerializer,
        "update": UsuarioSerializer,
        "partial_update": UsuarioSerializer,
        "convidar_usuario": ConvidarUsuarioSerializer,
        "aceitar_convite_usuario": UsuarioSerializer,
    }
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
        return Response({"mensagem": _("Usuário ativado")})

    @action(methods=["post"], detail=True)
    def inativar_usuario(self, request, pk):
        usuario = self.get_object()
        usuario.is_active = False
        usuario.save()
        return Response({"mensagem": _("Usuário inativado")})

    @action(methods=["post"], detail=False)
    def convidar_usuario(self, request, pk):
        return self.generic_action()

    @action(methods=["post"], detail=False)
    def aceitar_convite_usuario(self, request, pk):
        return self.generic_action()
