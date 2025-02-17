from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import (
    CategoriaProdutoViewSet,
    ComplementoProdutoViewSet,
    CustomizacaoProdutoItemViewSet,
    CustomizacaoProdutoViewSet,
    GrupoComplementoProdutoViewSet,
    ProdutoViewSet,
)

router_v1 = DefaultRouter()

router_v1.register("produtos", ProdutoViewSet, "produtos")
router_v1.register("categorias_produto", CategoriaProdutoViewSet, "categorias_produto")
router_v1.register("complementos_produtos", ComplementoProdutoViewSet, "complementos_produtos")
router_v1.register("grupos_complementos_produtos", GrupoComplementoProdutoViewSet, "grupos_complementos_produtos")
router_v1.register("custoamizacoes_produtos", CustomizacaoProdutoViewSet, "custoamizacoes_produtos")
router_v1.register("custoamizacoes_produtos_itens", CustomizacaoProdutoItemViewSet, "custoamizacoes_produtos_itens")

urlpatterns = [
    path("v1/", include(router_v1.urls)),
]
