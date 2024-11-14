from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import ComissaoGarcomViewSet

router_v1 = DefaultRouter()
router_v1.register("comissoes_garcons", ComissaoGarcomViewSet, "comissoes_garcons")

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
