from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import AcrescimoViewSet, CategoriaProdutoViewSet, GrupoAcrescimoProdutoViewSet, ProdutoViewSet

router_v1 = DefaultRouter()

router_v1.register("produtos", ProdutoViewSet, "produtos")
router_v1.register("categorias_produto", CategoriaProdutoViewSet, "categorias_produto")
router_v1.register("acrescimos_produtos", AcrescimoViewSet, "acrescimos_produtos")
router_v1.register("grupo_acrescimos_produto", GrupoAcrescimoProdutoViewSet, "grupo_acrescimos_produto")

urlpatterns = [
    path("v1/", include(router_v1.urls)),
]
