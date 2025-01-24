from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import UsuarioViewSet

router_auth = DefaultRouter()

router_v1 = DefaultRouter()
router_v1.register("usuarios", UsuarioViewSet, "usuarios")

urlpatterns = [
    path("auth/", include(router_auth.urls)),
    path("v1/", include(router_v1.urls)),
]
