from django.db.models import Count, F
from django.forms import model_to_dict
from django.utils import timezone

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.fidelidade.models import StatusCartaoFidelidadeChoices
from apps.system.base.views import BaseModelViewSet
from apps.vendas.services import gerar_venda_por_comanda

from .models import StatusComandaChoices, StatusComandaItemChoices
from .serializers import (
    AplicarCuponSerializer,
    Comanda,
    ComandaAlteracaoSerializer,
    ComandaCancelarSerializer,
    ComandaFinalizarSerializer,
    ComandaItem,
    ComandaItemAlteracaoSerializer,
    ComandaItemVisualizacaoSerializer,
    ComandaListSerializer,
    ComandaRetrieveSerializer,
)
from .services import (
    atualizar_codigo_comanda,
    baixar_estoque,
    criar_carimbo_cartao_fidelidade,
    gerar_comissao_garcom,
)


class ComandaViewSet(BaseModelViewSet):
    queryset = Comanda.objects.all()
    serializer_classes = {
        "list": ComandaListSerializer,
        "retrieve": ComandaRetrieveSerializer,
        "create": ComandaAlteracaoSerializer,
        "update": ComandaAlteracaoSerializer,
        "partial_update": ComandaAlteracaoSerializer,
        "visualizacao": ComandaRetrieveSerializer,
    }
    filterset_fields = {
        "id": ["exact"],
        "cm_status": ["exact", "in"],
        "cm_mesa": ["exact"],
        "cm_cliente": ["exact", "icontains"],
        "cm_cliente_fidelidade": ["exact"],
        "data_criacao": ["exact"],
    }

    def perform_create(self, serializer, **overwrite):
        super().perform_create(serializer)

        comanda = serializer.instance

        atualizar_codigo_comanda(comanda)

        if comanda.cm_mesa is not None:
            comanda.cm_mesa.ms_ocupada = True
            comanda.cm_mesa.save()

    @action(methods=["post"], detail=True)
    def finalizar(self, request, **kwargs):
        comanda = self.get_object()
        serializer = ComandaFinalizarSerializer(data=request.data, context={"comanda": comanda})
        serializer.is_valid(raise_exception=True)

        agora = timezone.now()

        comanda.cm_status = StatusComandaChoices.FINALIZADA
        comanda.cm_data_finalizacao = agora
        comanda.cm_hora_finalizacao = agora.time()
        comanda.save()

        if comanda.cm_mesa is not None:
            comanda.cm_mesa.ms_ocupada = False
            comanda.cm_mesa.save()

        if comanda.cm_garcom is not None:
            gerar_comissao_garcom(comanda)

        if comanda.cm_cartao_fidelidade:
            comanda.cm_cartao_fidelidade.cr_status = StatusCartaoFidelidadeChoices.RESGATADA
            comanda.cm_cartao_fidelidade.save()
        else:
            criar_carimbo_cartao_fidelidade(comanda)

        gerar_venda_por_comanda(comanda, request.user)

        return Response()

    @action(methods=["post"], detail=True)
    def cancelar(self, request, **kwargs):
        comanda = self.get_object()

        serializer = ComandaCancelarSerializer(data=request.data, context={"comanda": comanda})
        serializer.is_valid(raise_exception=True)

        agora = timezone.now()

        comanda.cm_status = StatusComandaChoices.CANCELADA
        comanda.cm_data_cancelamento = agora.date()
        comanda.cm_hora_cancelamento = agora.time()

        comanda.save()

        if comanda.cm_mesa is not None:
            comanda.cm_mesa.ms_ocupada = False
            comanda.cm_mesa.save()

        itens = comanda.itens.all()
        itens.update(ct_status=StatusComandaItemChoices.CANCELADO)

        return Response()

    @action(methods=["post"], detail=True)
    def aplicar_cupon(self, request, **kwargs):
        comanda = self.get_object()
        serializer = AplicarCuponSerializer(data=request.data, context={"comanda": comanda})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response()

    @action(methods=["get"], detail=True)
    def visualizar(self, request, **kwargs):
        comanda = self.get_object()
        queryset = (
            ComandaItem.objects.filter(ct_comanda=comanda)
            .values(
                "ct_produto",
                "ct_produto__pr_nome",
                "ct_produto__pr_url_imagem",
                "ct_preco_unitario_produto",
            )
            .annotate(ct_quantidade_total_produto=Count(F("id")))
            .annotate(
                ct_valor_total_produto=Count(F("id")) * F("ct_preco_unitario_produto")
            )
        )

        dados_comanda = model_to_dict(comanda)
        dados_comanda["cm_valor_total"] = comanda.cm_valor_total
        dados_comanda["cm_valor_comissao_garcom"] = comanda.cm_valor_comissao
        dados_comanda["cm_itens"] = queryset

        return Response(dados_comanda)


class ItemComandaViewSet(BaseModelViewSet):
    queryset = ComandaItem.objects.all()
    serializer_classes = {
        "list": ComandaItemVisualizacaoSerializer,
        "retrieve": ComandaItemVisualizacaoSerializer,
        "create": ComandaItemAlteracaoSerializer,
        "update": ComandaItemAlteracaoSerializer,
        "partial_update": ComandaItemAlteracaoSerializer,
        "bulk_create": ComandaItemAlteracaoSerializer,
    }
    filterset_fields = {
        "ct_comanda": ["exact"],
        "ct_comanda__cm_status": ["exact"],
        "ct_comanda__data_criacao": ["exact"],
        "ct_status": ["exact"],
        "ct_produto__pr_tempo_preparo": ["gt"],
    }

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["vincular_num_pedido"] = self.action == "bulk_create"
        return context

    @action(methods=["post"], detail=True)
    def preparar(self, request, *args, **kwargs):
        agora = timezone.now()

        instance = self.get_object()

        instance.ct_status = StatusComandaItemChoices.PREPARANDO
        instance.ct_data_preparamento = agora
        instance.ct_hora_preparamento = agora

        instance.save()

        return Response()

    @action(methods=["post"], detail=True)
    def finalizar(self, request, *args, **kwargs):
        agora = timezone.now()

        instance = self.get_object()

        instance.ct_status = StatusComandaItemChoices.PRONTO
        instance.ct_data_finalizacao = agora
        instance.ct_hora_finalizacao = agora

        instance.save()

        return Response()

    @action(methods=["post"], detail=True)
    def entregar(self, request, *args, **kwargs):
        agora = timezone.now()

        instance = self.get_object()
        instance.ct_status = StatusComandaItemChoices.ENTREGUE
        instance.ct_data_entregue = agora
        instance.ct_hora_entregue = agora

        instance.save()

        baixar_estoque(instance)

        return Response()

    @action(methods=["post"], detail=True)
    def cancelar(self, request, *args, **kwargs):
        agora = timezone.now()

        instance = self.get_object()
        instance.ct_status = StatusComandaItemChoices.CANCELADO
        instance.ct_data_entregue = agora
        instance.ct_hora_entregue = agora

        instance.save()

        return Response()


class PainelPedidosViewSet(GenericViewSet):
    def list(self, request):
        numeros_pedidos = (
            ComandaItem.objects.filter(
                data_criacao=timezone.now(),
                ct_status__in=(
                    StatusComandaItemChoices.ABERTO,
                    StatusComandaItemChoices.PREPARANDO,
                    StatusComandaItemChoices.PRONTO,
                ),
            )
            .distinct("ct_pedido")
            .order_by("ct_pedido")
            .values_list("ct_pedido", flat=True)
        )

        status_finalizado = (
            StatusComandaItemChoices.PRONTO,
            StatusComandaItemChoices.ENTREGUE,
        )

        pedidos = {
            "preparando": [],
            "prontos": [],
        }

        for num_pedido in numeros_pedidos:
            itens_comanda = ComandaItem.objects.filter(
                ct_pedido=num_pedido,
                data_criacao=timezone.now(),
            )

            itens_pedido = []
            pedido_pronto = True

            for item in itens_comanda:
                itens_pedido.append(
                    {
                        "id": item.pk,
                        "pronto": item.ct_status in status_finalizado,
                        "produto": item.ct_produto.pr_nome,
                    }
                )

                if item.ct_status not in status_finalizado:
                    pedido_pronto = False

            if pedido_pronto:
                pedidos["prontos"].append(
                    {
                        "pedido": num_pedido,
                        "itens": itens_pedido,
                    }
                )
            else:
                pedidos["preparando"].append(
                    {
                        "pedido": num_pedido,
                        "itens": itens_pedido,
                    }
                )

        return Response({"pedidos": pedidos})
