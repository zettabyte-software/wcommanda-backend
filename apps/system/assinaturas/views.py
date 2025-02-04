import logging

from django.conf import settings

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

import stripe
from django_multitenant.utils import set_current_tenant

from apps.system.base.views import BaseModelViewSet, BaseViewSet

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
    }


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


class StripeWebhookViewSet(BaseViewSet):
    permission_classes = [AllowAny]

    def create(self, request):
        payload = request.body
        sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")
        endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

        try:
            # Verifica e constrói o objeto de evento do Stripe
            event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
        except ValueError:
            # Payload inválido
            return Response({"error": "Invalid payload"}, status=status.HTTP_400_BAD_REQUEST)
        except stripe.error.SignatureVerificationError:
            # Assinatura inválida
            return Response({"error": "Invalid signature"}, status=status.HTTP_400_BAD_REQUEST)

        # Tratamento dos diferentes tipos de evento
        if event["type"] == "checkout.session.completed":
            session = event["data"]["object"]
            # Aqui você pode processar o pagamento confirmado, por exemplo, atualizar o status do pedido
            self.handle_checkout_session(session)
        elif event["type"] == "payment_intent.succeeded":
            payment_intent = event["data"]["object"]
            # Processa o pagamento confirmado via PaymentIntent
            self.handle_payment_intent(payment_intent)
        else:
            # Se o evento não for de interesse, pode apenas logar ou ignorar
            pass

        # Retorna 200 para confirmar o recebimento do webhook
        return Response(status=status.HTTP_200_OK)

    def handle_checkout_session(self, session):
        """
        Processa o evento 'checkout.session.completed'.
        Exemplo: Atualize o status do pedido no seu sistema com base na session.
        """

        # Exemplo de extração de dados:
        customer_email = session.get("customer_details", {}).get("email")
        payment_status = session.get("payment_status")
        # Lógica para atualizar o pedido no banco de dados...
        logger.info(f"Checkout Session completed para {customer_email} com status {payment_status}")

    def handle_payment_intent(self, payment_intent):
        """
        Processa o evento 'payment_intent.succeeded'.
        Exemplo: Atualize o status do pagamento com base no payment_intent.
        """
        # Exemplo de extração de dados:
        amount_received = payment_intent.get("amount_received")
        currency = payment_intent.get("currency")
        # Lógica para atualizar o pagamento no banco de dados...
        logger.info(f"PaymentIntent succeeded com {amount_received} {currency}")
