from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import FilaEsperaClienteViewSet, FilaViewSet

router_v1 = DefaultRouter()
router_v1.register("fila_espera", FilaViewSet, "fila_espera")
router_v1.register("fila_espera_cliente", FilaEsperaClienteViewSet, "fila_espera_cliente")


urlpatterns = [
    path("v1/", include(router_v1.urls)),
]
