from django.db.models import Max

from rest_framework.decorators import action
from rest_framework.response import Response

from apps.comandas.serializers import Comanda, ComandaRetrieveSerializer
from apps.system.base.views import BaseModelViewSet

from .serializers import Mesa, MesaAlteracaoSerializer, MesaVisualizacaoSerializer


class MesaViewSet(BaseModelViewSet):
    queryset = Mesa.objects.all()
    serializer_classes = {
        "list": MesaVisualizacaoSerializer,
        "retrieve": MesaVisualizacaoSerializer,
        "create": MesaAlteracaoSerializer,
        "update": MesaAlteracaoSerializer,
        "partial_update": MesaAlteracaoSerializer,
        "comandas": ComandaRetrieveSerializer,
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

    @action(methods=["get"], detail=True)
    def comandas(self, request):
        mesa = self.get_object()
        comandas = Comanda.objects.filter(cm_mesa=mesa)
        serializer = self.get_serializer(comandas, many=True)
        return self.get_paginated_response(serializer.data)
