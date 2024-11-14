from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import MesaViewSet

router_v1 = DefaultRouter()
router_v1.register("mesas", MesaViewSet)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
