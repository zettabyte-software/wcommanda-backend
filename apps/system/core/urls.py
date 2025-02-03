from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import ImTeapootViewSet

router_v1 = DefaultRouter()
router_v1.register("i_am_a_teapoot", ImTeapootViewSet, "i_am_a_teapoot")

urlpatterns = [
    path("v1/", include(router_v1.urls)),
]
