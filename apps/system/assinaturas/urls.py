from django.conf import settings
from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import AssinaturaViewSet, CriarAssinaturaViewSet, PlanoViewSet, StripeWebhookViewSet

router_v1 = DefaultRouter()

router_v1.register("criar_assinatura", CriarAssinaturaViewSet, "criar_assinatura")
router_v1.register("stripe/webhook", StripeWebhookViewSet, "checkout_stripe")

if settings.IN_DEVELOPMENT:
    router_v1.register("assinaturas", AssinaturaViewSet, "assinaturas")
    router_v1.register("planos", PlanoViewSet, "planos")

urlpatterns = [
    path("v1/", include(router_v1.urls)),
]
