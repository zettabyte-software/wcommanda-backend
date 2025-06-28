import logging

from django.conf import settings

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ViewSet

import stripe
from django_multitenant.utils import get_current_tenant, set_current_tenant

from apps.system.base.views import BaseModelViewSet
from utils.env import get_env_var

from .serializers import (
    Assinatura,
    AssinaturaAlteracaoSerializer,
    AssinaturaVisualizacaoSerializer,
    CriarAssinaturaSerializer,
    Plano,
    PlanoAlteracaoSerializer,
    PlanoVisualizacaoSerializer,
)

logger = logging.getLogger(__name__)


class AssinaturaViewSet(BaseModelViewSet):
    queryset = Assinatura.objects.all()
    serializer_classes = {
        "list": AssinaturaVisualizacaoSerializer,
        "retrieve": AssinaturaVisualizacaoSerializer,
        "create": AssinaturaAlteracaoSerializer,
        "update": AssinaturaAlteracaoSerializer,
        "partial_update": AssinaturaAlteracaoSerializer,
        "bulk_create": AssinaturaAlteracaoSerializer,
        "info": AssinaturaVisualizacaoSerializer,
    }

    @action(detail=False, methods=["get"])
    def info(self, request):
        assinatura = get_current_tenant()
        if not assinatura:
            return Response({"mensagem": "Nenhuma assinatura encontrada"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(assinatura)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PlanoViewSet(BaseModelViewSet):
    queryset = Plano.objects.all()
    serializer_classes = {
        "list": PlanoVisualizacaoSerializer,
        "retrieve": PlanoVisualizacaoSerializer,
        "create": PlanoAlteracaoSerializer,
        "update": PlanoAlteracaoSerializer,
        "partial_update": PlanoAlteracaoSerializer,
        "bulk_create": PlanoAlteracaoSerializer,
    }


class CriarAssinaturaViewSet(ViewSet):
    permission_classes = [AllowAny]
    authentication_classes = []

    def create(self, request):
        set_current_tenant(None)
        serializer = CriarAssinaturaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)


class StripeWebhookViewSet(GenericViewSet):
    permission_classes = [AllowAny]

    def create(self, request):
        payload = request.body
        sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")
        endpoint_secret = get_env_var("STRIPE_WEBHOOK_SECRET")

        try:
            event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
        except ValueError:
            logger.error("Payload inválido")
            return Response({"error": "Invalid payload"}, status=status.HTTP_400_BAD_REQUEST)
        except stripe.error.SignatureVerificationError:
            logger.error("Assinatura inválida")
            return Response({"error": "Invalid signature"}, status=status.HTTP_400_BAD_REQUEST)

        if event["type"] == "invoice.payment_succeeded":
            self.handle_payment_succeeded()

        return Response(status=status.HTTP_200_OK)

    def handle_payment_succeeded(self):
        pass
