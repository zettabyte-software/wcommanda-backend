import logging

from django.db.models import Count, F
from django.utils import timezone

from threadlocals.threadlocals import get_current_user

from apps.estoque.models import MovimentacaoEstoque, TiposMovimentacaoEstoqueChoices
from apps.fidelidade.models import Carimbo, CartaoFidelidade, StatusCartaoFidelidadeChoices
from apps.fidelidade.services import enviar_email_cartao_fidelidade_completo
from apps.financeiro.models import Pagamento
from apps.garcons.models import ComissaoGarcom
from apps.system.conf.services import get_configuracao
from apps.vendas.models import Venda, VendaItem

from .models import Comanda, ComandaItem, StatusComandaChoices

logger = logging.getLogger(__name__)


def vincular_num_pedido(itens):
    """Atribui um número de pedido sequencial a um conjunto de itens com base na data atual.

    Esta função recupera o último número de pedido criado hoje e o incrementa em um
    para atribuir um novo número de pedido aos itens fornecidos. Se nenhum pedido foi criado hoje,
    começa com o número de pedido 1.

    Args:
        itens (QuerySet): Um QuerySet do Django de itens a serem atualizados com o novo número de pedido.

    Return:
        None

    """
    ultimo_pedido_hoje = ComandaItem.objects.filter(data_criacao=timezone.now()).order_by("-id").first()
    pedido = None
    if ultimo_pedido_hoje is None:
        pedido = 1
    else:
        pedido = ultimo_pedido_hoje.ct_pedido + 1

    itens.update(ct_pedido=pedido)


def baixar_estoque(comanda_item: ComandaItem):
    """Baixa o estoque de um item da comanda, caso o produto controle estoque e não haja movimentação de estoque para o item.

    Args:
        comanda_item (ComandaItem): O item da comanda que terá o estoque baixado.

    Return:
        None

    """
    if not comanda_item.ct_produto.pr_controla_estoque:
        return

    movimentacao_comanda_item = MovimentacaoEstoque.objects.filter(mv_comanda_item=comanda_item).first()
    if movimentacao_comanda_item is not None:
        return

    # caso não tenha uma movimentação de estoque para o produto, ele não possui estoque
    ultima_movimentacao_produto = MovimentacaoEstoque.objects.filter(mv_produto=comanda_item.ct_produto).first()
    if not ultima_movimentacao_produto:
        return

    baixa_estoque = MovimentacaoEstoque()
    baixa_estoque.mv_comanda_item = comanda_item
    baixa_estoque.mv_tipo = TiposMovimentacaoEstoqueChoices.SAIDA
    baixa_estoque.mv_produto = comanda_item.ct_produto
    baixa_estoque.mv_quantidade = 1
    baixa_estoque.mv_quantidade_anterior = ultima_movimentacao_produto.mv_quantidade_atual
    baixa_estoque.mv_quantidade_atual = ultima_movimentacao_produto.mv_quantidade_atual - 1
    baixa_estoque.save()


def atualizar_codigo_comanda(comanda: Comanda):
    """Atualiza o código da comanda com base na configuração de reinício de código.

    Se a configuração "WCM_REINICIO_CODIGO_COMANDA" estiver habilitada, o código da comanda será reiniciado diariamente.
    Caso contrário, o código da comanda será incrementado com base na última comanda criada.

    Args:
        comanda (Comanda): A instância da comanda que será atualizada.

    Returns:
        None

    """
    reinicia_codigo = get_configuracao("WCM_REINICIO_CODIGO_COMANDA")

    if reinicia_codigo:
        ultima_comanda_hoje = Comanda.objects.filter(data_criacao=timezone.now()).exclude(id=comanda.pk).first()

        if ultima_comanda_hoje is not None:
            comanda.cm_codigo = ultima_comanda_hoje.cm_codigo + 1
    else:
        ultima_comanda = Comanda.objects.exclude(id=comanda.pk).first()

        if ultima_comanda is not None:
            comanda.cm_codigo = ultima_comanda.cm_codigo + 1


    comanda.save()


def gerar_comissao_garcom(comanda: Comanda):
    """Gera uma comissão para o garçom com base na comanda fornecida.

    Args:
        comanda (Comanda): A comanda para a qual a comissão será gerada.

    Returns:
        ComissaoGarcom: Um objeto ComissaoGarcom criado com os dados da comanda.

    Exceções:
        Pode lançar exceções relacionadas à criação do objeto ComissaoGarcom ou à obtenção da configuração do percentual de comissão.

    """
    percentual_comissao = get_configuracao("WCM_PERCENTUAL_COMISSAO_GARCON")
    return ComissaoGarcom.objects.create(
        cg_garcom=comanda.cm_garcom,
        cg_comanda=comanda,
        cg_valor_total_comanda=comanda.cm_valor_total,
        cg_valor=comanda.cm_valor_comissao,
        cg_percentual=percentual_comissao,
        owner=get_current_user(),
    )


def criar_carimbo_cartao_fidelidade(comanda: Comanda):
    """Cria um carimbo no cartão de fidelidade associado a uma comanda, se as condições forem atendidas.

    Args:
        comanda (Comanda): A comanda para a qual o carimbo será criado.

    Returns:
        None

    Conditions:
        - O cartão de fidelidade deve estar com status 'ABERTA' e não deve estar expirado.
        - Se houver um produto específico na condição do prêmio, a comanda deve conter esse produto.
        - Se houver um valor mínimo na condição do prêmio, o valor total da comanda deve ser maior ou igual a esse valor.

    Side Effects:
        - Cria um novo carimbo no cartão de fidelidade.
        - Se o total de carimbos atingir a quantidade necessária para o prêmio, o status do cartão de fidelidade é atualizado para 'COMPLETO'.
        - Se o cliente associado ao cartão de fidelidade tiver um e-mail, um e-mail de notificação é enviado informando que o cartão está completo.

    """

    cartao_fidelidade = CartaoFidelidade.objects.filter(
        cr_status=StatusCartaoFidelidadeChoices.ABERTA,
        cr_cliente=comanda.cm_cliente_fidelidade,
    ).first()

    if not cartao_fidelidade or cartao_fidelidade.cr_expirado:
        return

    condicao_premio = cartao_fidelidade.cr_condicao_premio
    if condicao_premio.cn_produto:
        comprou_produto_condicao = ComandaItem.objects.filter(ct_comanda=comanda, ct_produto=condicao_premio.cn_produto).exists()
        if not comprou_produto_condicao:
            return

    if condicao_premio.cn_valor_minimo:
        if condicao_premio.cn_valor_minimo > comanda.cm_valor_total:
            return

    Carimbo.objects.create(cb_cartao_fidelidade=cartao_fidelidade)

    if cartao_fidelidade.cr_total_carimbos == cartao_fidelidade.cr_condicao_premio.cn_quantidade:
        cartao_fidelidade.cr_status = StatusCartaoFidelidadeChoices.COMPLETO
        cartao_fidelidade.save()

        if cartao_fidelidade.cr_cliente.cl_email:
            enviar_email_cartao_fidelidade_completo(cartao_fidelidade)


def gerar_venda_por_comanda(comanda: Comanda):
    """Gera uma venda a partir de uma comanda.

    Args:
        comanda (Comanda): A comanda a partir da qual a venda será gerada.

    Returns:
        Venda: A venda gerada a partir da comanda.

    Este método realiza as seguintes operações:
    1. Cria uma instância de Venda com base nas informações da comanda.
    2. Salva a instância de Venda no banco de dados.
    3. Agrupa os itens da comanda por produto e cria instâncias de VendaItem para cada grupo.
    4. Cria uma instância de Pagamento associada à venda gerada.

    Observations:
        A função assume que as classes Comanda, Venda, ComandaItem, VendaItem e Pagamento, 
        bem como os métodos get_current_user e F, estão definidos e importados no contexto onde esta função é utilizada.

    """
    venda = Venda(
        vn_comanda=comanda,
        vn_cliente=comanda.cm_cliente,
        vn_cliente_fidelidade=comanda.cm_cliente_fidelidade,
        vn_valor_total=comanda.cm_valor_total,
        owner=get_current_user(),
    )

    venda.save()

    itens_comanda_por_produto = (
        ComandaItem.objects.filter(ct_comanda=comanda)
        .values("ct_produto")
        .annotate(quantidade=Count("ct_produto"), preco_unitario=F("ct_preco_unitario_produto"))
    )
    for item in itens_comanda_por_produto:
        VendaItem.objects.create(
            vd_venda=venda,
            vd_quantidade=item["quantidade"],
            vd_produto_id=item["ct_produto"],
            vd_preco_unitario_produto=item["preco_unitario"],
            vd_valor_total=item["preco_unitario"] * item["quantidade"],
            owner=get_current_user(),
        )

    Pagamento.objects.create(
        pg_venda=venda,
        pg_parcela=1,
        pg_valor=comanda.cm_valor_total,
        pg_forma_pagamento=comanda.cm_forma_pagamento,
        owner=get_current_user(),
    )

    return venda


def finalizar_comanda(comanda: Comanda):
    """Finaliza uma comanda, atualizando seu status e registrando a data e hora de finalização.

    Args:
        comanda (Comanda): A instância da comanda a ser finalizada.

    Actions:
    - Atualiza o status da comanda para 'FINALIZADA'.
    - Registra a data e hora de finalização da comanda.
    - Libera a mesa associada à comanda, se houver.
    - Gera a comissão para o garçom associado à comanda, se houver.
    - Cria um carimbo no cartão de fidelidade do cliente, se aplicável.
    - Atualiza o status do cartão de fidelidade da comanda para 'RESGATADA', se houver.
    - Gera a venda correspondente à comanda.

    """
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

    if comanda.cm_cliente_fidelidade:
        criar_carimbo_cartao_fidelidade(comanda)

    if comanda.cm_cartao_fidelidade:
        comanda.cm_cartao_fidelidade.cr_status = StatusCartaoFidelidadeChoices.RESGATADA
        comanda.cm_cartao_fidelidade.save()

    gerar_venda_por_comanda(comanda)
