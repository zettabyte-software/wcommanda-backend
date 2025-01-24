from apps.system.base.views import BaseModelViewSet

from .serializers import (
    Notificacao,
    NotificacaoAlteracaoSerializer,
    NotificacaoVisualizacaoSerializer,
)


class NotificacaoViewSet(BaseModelViewSet):
    queryset = Notificacao.objects.all()
    serializer_classes = {
        "list": NotificacaoVisualizacaoSerializer,
        "retrieve": NotificacaoVisualizacaoSerializer,
        "create": NotificacaoAlteracaoSerializer,
        "update": NotificacaoAlteracaoSerializer,
        "partial_update": NotificacaoAlteracaoSerializer,
        "bulk_create": NotificacaoAlteracaoSerializer,
    }
