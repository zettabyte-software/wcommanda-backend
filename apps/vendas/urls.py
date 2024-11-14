from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import DashboardVendasViewSet

router_v1 = DefaultRouter()
router_v1.register("vendas", DashboardVendasViewSet, "dashboard_vendas")

urlpatterns = [
    path('v1/dashboards/', include(router_v1.urls)),
]
