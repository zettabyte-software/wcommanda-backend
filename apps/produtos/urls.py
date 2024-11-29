from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import AcrescimoProdutoViewSet, AcrescimoViewSet, CategoriaProdutoViewSet, ProdutoViewSet

router_v1 = DefaultRouter()

router_v1.register("produtos", ProdutoViewSet, "produtos")
router_v1.register("categorias_produto", CategoriaProdutoViewSet, "categorias_produto")
router_v1.register("acrescimos", AcrescimoViewSet, "acrescimos")
router_v1.register("acrescimos_produto", AcrescimoProdutoViewSet, "acrescimos_produto")

urlpatterns = [
    path("v1/", include(router_v1.urls)),
]
