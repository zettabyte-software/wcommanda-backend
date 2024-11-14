from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    ProdutoViewSet,
    CategoriaProdutoViewSet,
)

router_v1 = DefaultRouter()

router_v1.register("produtos", ProdutoViewSet)
router_v1.register("categorias_produto", CategoriaProdutoViewSet)

urlpatterns = [
    path("v1/", include(router_v1.urls)),
]
