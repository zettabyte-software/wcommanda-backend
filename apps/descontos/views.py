from rest_framework.decorators import action
from rest_framework.response import Response

from apps.system.base.views import BaseModelViewSet

from .serializers import (
    CuponDesconto,
    CuponDescontoAlteracaoSerializer,
    CuponDescontoVisualizacaoSerializer,
    GerarCuponAniversarioSerializer,
)


class CuponDescontoViewSet(BaseModelViewSet):
    queryset = CuponDesconto.objects.all()
    serializer_classes = {
        "list": CuponDescontoVisualizacaoSerializer,
        "retrieve": CuponDescontoVisualizacaoSerializer,
        "create": CuponDescontoAlteracaoSerializer,
        "update": CuponDescontoAlteracaoSerializer,
        "partial_update": CuponDescontoAlteracaoSerializer,
    }

    @action(methods=["get"], detail=True)
    def gerar_cupon_aniversario(self, request, pk):
        serializer = GerarCuponAniversarioSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cupon = serializer.save()
        serializer_visualizacao = CuponDescontoVisualizacaoSerializer(cupon)
        return Response(serializer_visualizacao.data)
