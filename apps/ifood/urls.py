from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import IfoodViewSet

router_v1 = DefaultRouter()
router_v1.register('ifood', IfoodViewSet, 'ifood')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
