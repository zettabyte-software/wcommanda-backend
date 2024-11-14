from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import EstoqueAtualViewSet, MovimentacaoEstoqueViewSet

router_v1 = DefaultRouter()
router_v1.register("movimentacoes_estoque", MovimentacaoEstoqueViewSet)
router_v1.register("estoque_atual", EstoqueAtualViewSet, "estoque_atual")

urlpatterns = [
    path("v1/", include(router_v1.urls)),
]
