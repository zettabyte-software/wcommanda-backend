from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import (
    PremioViewSet,
    PremioItemViewSet,
    CartaoFidelidadeViewSet,
    CarimboViewSet,
    CondicaoPremioViewSet,
)

router_v1 = DefaultRouter()
router_v1.register("premios", PremioViewSet, "premios")
router_v1.register("itens_premio", PremioItemViewSet, "itens_premio")
router_v1.register("cartoes_fidelidade", CartaoFidelidadeViewSet, "cartoes_fidelidade")
router_v1.register("carimbos", CarimboViewSet, "carimbos")
router_v1.register("condicoes_premio", CondicaoPremioViewSet, "condicoes_premio")

urlpatterns = [
    path("v1/", include(router_v1.urls)),
]
