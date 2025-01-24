from django.conf import settings
from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import AmbienteViewSet, CriarAssinaturaViewSet

router_v1 = DefaultRouter()
router_v1.register("criar_assinatura", CriarAssinaturaViewSet, "criar_assinatura")

if settings.IN_DEVELOPMENT:
    router_v1.register("ambientes", AmbienteViewSet, "ambientes")

urlpatterns = [
    path("v1/", include(router_v1.urls)),
]
