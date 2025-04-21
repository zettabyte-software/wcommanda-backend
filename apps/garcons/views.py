from rest_framework.decorators import action
from rest_framework.response import Response

from apps.system.base.views import BaseModelViewSet

from .models import StatusComissaoGarcomChoices
from .serializers import (
    ComissaoGarcom,
    ComissaoGarcomAlteracaoSerializer,
    ComissaoGarcomVisualizacaoSerializer,
)


class ComissaoGarcomViewSet(BaseModelViewSet):
    queryset = ComissaoGarcom.objects.all()
    serializer_classes = {
        "list": ComissaoGarcomVisualizacaoSerializer,
        "retrieve": ComissaoGarcomVisualizacaoSerializer,
        "create": ComissaoGarcomAlteracaoSerializer,
        "update": ComissaoGarcomAlteracaoSerializer,
        "partial_update": ComissaoGarcomAlteracaoSerializer,
    }
    filterset_fields = {
        "id": ["exact"],
        "cg_valor": ["exact"],
        "cg_garcom__first_name": ["icontains"],
        "cg_valor_total_comanda": ["exact"],
        "cg_comanda__cm_codigo": ["exact"],
        "cg_comanda__data_criacao": ["exact"],
        "owner": ["exact"],
    }

    @action(methods=["post"], detail=True)
    def efetuar_comissao(self, request):
        comissao = self.get_object()
        comissao.cg_status = StatusComissaoGarcomChoices.EFETUADA
        comissao.save()
        serializer = ComissaoGarcomVisualizacaoSerializer(comissao)
        return Response(serializer.data)

    @action(methods=["post"], detail=True)
    def estornar_comissao(self, request):
        comissao = self.get_object()
        comissao.cg_status = StatusComissaoGarcomChoices.ESTORNADA
        comissao.save()
        serializer = ComissaoGarcomVisualizacaoSerializer(comissao)
        return Response(serializer.data)

    @action(methods=["post"], detail=True)
    def cancelar_comissao(self, request):
        comissao = self.get_object()
        comissao.cg_status = StatusComissaoGarcomChoices.CANCELADA
        comissao.save()
        serializer = ComissaoGarcomVisualizacaoSerializer(comissao)
        return Response(serializer.data)
