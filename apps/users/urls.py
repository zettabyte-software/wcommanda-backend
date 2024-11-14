from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import UsuarioViewSet, CadastroViewSet

router_auth = DefaultRouter()
router_auth.register("cadastro", CadastroViewSet, "cadastro")

router_v1 = DefaultRouter()
router_v1.register("usuarios", UsuarioViewSet, "usuarios")

urlpatterns = [
    path("auth/", include(router_auth.urls)),
    path("v1/", include(router_v1.urls)),
]
