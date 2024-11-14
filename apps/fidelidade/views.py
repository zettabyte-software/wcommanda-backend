from rest_framework.decorators import action
from rest_framework.response import Response

from apps.system.base.views import BaseModelViewSet

from .serializers import (
    Carimbo,
    CarimboAlteracaoSerializer,
    CarimboVisualizacaoSerializer,
    CartaoFidelidade,
    CartaoFidelidadeAlteracaoSerializer,
    CartaoFidelidadeVisualizacaoSerializer,
    CondicaoPremio,
    CondicaoPremioAlteracaoSerializer,
    CondicaoPremioVisualizacaoSerializer,
    EnviarLinkCartaoFidelidadeSerializer,
    Premio,
    PremioAlteracaoSerializer,
    PremioItem,
    PremioItemAlteracaoSerializer,
    PremioItemVisualizacaoSerializer,
    PremioVisualizacaoSerializer,
)


class CartaoFidelidadeViewSet(BaseModelViewSet):
    queryset = CartaoFidelidade.objects.all()
    serializer_classes = {
        "list": CartaoFidelidadeVisualizacaoSerializer,
        "retrieve": CartaoFidelidadeVisualizacaoSerializer,
        "create": CartaoFidelidadeAlteracaoSerializer,
        "update": CartaoFidelidadeAlteracaoSerializer,
        "partial_update": CartaoFidelidadeAlteracaoSerializer,
        "enviar": EnviarLinkCartaoFidelidadeSerializer,
    }
    filterset_fields = {
        "cr_status": ["exact", "icontains", "in"],
        "cr_cliente": ["exact"],
        "cr_codigo": ["exact"],
    }
    search_fields = (
        "cr_cliente__cl_nome",
        "cr_cliente__cl_sobrenome",
        "cr_Premio__pm_nome",
    )

    @action(methods=["post"], detail=False)
    def enviar(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response()


class CarimboViewSet(BaseModelViewSet):
    queryset = Carimbo.objects.all()
    serializer_classes = {
        "list": CarimboVisualizacaoSerializer,
        "retrieve": CarimboVisualizacaoSerializer,
        "create": CarimboAlteracaoSerializer,
        "update": CarimboAlteracaoSerializer,
        "partial_update": CarimboAlteracaoSerializer,
    }


class PremioViewSet(BaseModelViewSet):
    queryset = Premio.objects.all()
    serializer_classes = {
        "list": PremioVisualizacaoSerializer,
        "retrieve": PremioVisualizacaoSerializer,
        "create": PremioAlteracaoSerializer,
        "update": PremioAlteracaoSerializer,
        "partial_update": PremioAlteracaoSerializer,
    }


class PremioItemViewSet(BaseModelViewSet):
    queryset = PremioItem.objects.all()
    serializer_classes = {
        "list": PremioItemVisualizacaoSerializer,
        "retrieve": PremioItemVisualizacaoSerializer,
        "create": PremioItemAlteracaoSerializer,
        "update": PremioItemAlteracaoSerializer,
        "partial_update": PremioItemAlteracaoSerializer,
    }
    filterset_fields = {
        "pt_premio": ["exact"],
        "pt_produto": ["exact"],
    }
    ordering_fields = ("id",)


class CondicaoPremioViewSet(BaseModelViewSet):
    queryset = CondicaoPremio.objects.all()
    serializer_classes = {
        "list": CondicaoPremioVisualizacaoSerializer,
        "retrieve": CondicaoPremioVisualizacaoSerializer,
        "create": CondicaoPremioAlteracaoSerializer,
        "update": CondicaoPremioAlteracaoSerializer,
        "partial_update": CondicaoPremioAlteracaoSerializer,
    }
