from django.conf import settings
from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import AssinaturaViewSet, PlanoViewSet

router_v1 = DefaultRouter()

if settings.IN_DEVELOPMENT:
    router_v1.register("assinaturas", AssinaturaViewSet, "assinaturas")
    router_v1.register("planos", PlanoViewSet, "planos")

urlpatterns = [
    path("v1/", include(router_v1.urls)),
]
