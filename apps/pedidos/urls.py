from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import PedidoItemViewSet, PedidoViewSet

router_v1 = DefaultRouter()
router_v1.register("pedido", PedidoViewSet, "pedido")
router_v1.register("pedidos_itens", PedidoItemViewSet, "pedidos_itens")

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
