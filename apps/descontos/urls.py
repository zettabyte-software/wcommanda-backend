from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CuponDescontoViewSet

router_v1 = DefaultRouter()
router_v1.register("cupons_descontos", CuponDescontoViewSet, "cupons_descontos")

urlpatterns = [
    path("v1/", include(router_v1.urls)),
]
