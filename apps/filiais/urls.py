from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FilialViewSet

router_v1 = DefaultRouter()
router_v1.register("filiais", FilialViewSet, "filiais")

urlpatterns = [
    path("v1/", include(router_v1.urls)),
]
