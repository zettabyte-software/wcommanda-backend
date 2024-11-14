from django.db.models import Max

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.system.base.views import BaseModelViewSet
from .serializers import (
    Mesa,
    MesaVisualizacaoSerializer,
    MesaAlteracaoSerializer,
)


class MesaViewSet(BaseModelViewSet):
    queryset = Mesa.objects.all()
    serializer_classes = {
        "list": MesaVisualizacaoSerializer,
        "retrieve": MesaVisualizacaoSerializer,
        "create": MesaAlteracaoSerializer,
        "update": MesaAlteracaoSerializer,
        "partial_update": MesaAlteracaoSerializer,
    }
    filterset_fields = {
        "ms_quantidade_lugares": ["icontains"],
        "ms_ocupada": ["exact"],
        "ms_observacao": ["icontains"],
    }

    @action(methods=["get"], detail=False)
    def sugestao_codigo(self, request):
        codigo = Mesa.objects.aggregate(codigo=Max("ms_codigo"))["codigo"] or 0
        return Response({"ms_codigo": codigo + 1})
