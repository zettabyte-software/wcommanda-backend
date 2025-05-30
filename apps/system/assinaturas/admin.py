from django.contrib import admin

from .models import Assinatura, Plano


@admin.register(Assinatura)
class AssinaturaAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "ss_nome",
        "ss_subdominio",
        "ss_status",
        "ss_plano__pl_nome",
        "ss_plano__pl_tier",
        "ss_plano__pl_numero_usuarios",
        "ss_plano__pl_numero_telas",
        "ss_plano__pl_integra_ifood",
        "ss_plano__pl_limite_integracoes_pedidos_ifood",
        "ss_plano__pl_valor_mensalidade",
        "data_criacao",
        "hora_criacao",
    )
    list_filter = ("ss_status",)
    search_fields = (
        "ss_nome",
        "ss_subdominio",
        "ss_codigo_licenca",
    )
    ordering = ("-id",)
    list_per_page = 25


@admin.register(Plano)
class PlanoAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "pl_nome",
        "pl_tier",
        "pl_numero_usuarios",
        "pl_numero_telas",
        "pl_integra_ifood",
        "pl_limite_integracoes_pedidos_ifood",
        "pl_valor_mensalidade",
        "pl_observacao",
    )
    list_filter = ("pl_tier",)
    search_fields = (
        "pl_nome",
        "pl_observacao",
    )
    ordering = ("-id",)
    list_per_page = 25
