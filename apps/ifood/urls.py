from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import IntegracaoIfoodViewSet, PedidoIfoodViewSet

router_v1 = DefaultRouter()
router_v1.register('sincronizacao', IntegracaoIfoodViewSet, 'ifood_sincronizacao')
router_v1.register('pedidos', PedidoIfoodViewSet, 'ifood_pedidos')

urlpatterns = [
    path('v1/ifood/', include(router_v1.urls)),
]
