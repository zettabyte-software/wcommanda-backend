from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import ComandaViewSet, ItemComandaViewSet, PainelPedidosViewSet

router_v1 = DefaultRouter()

router_v1.register("comandas", ComandaViewSet, "comandas")
router_v1.register("itens_comanda", ItemComandaViewSet, "itens_comanda")
router_v1.register("painel_pedidos", PainelPedidosViewSet, "painel_pedidos")

urlpatterns = [
    path("v1/", include(router_v1.urls)),
]
