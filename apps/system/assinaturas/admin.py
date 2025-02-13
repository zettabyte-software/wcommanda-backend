from django.contrib import admin

from .models import Assinatura, Plano


@admin.register(Assinatura)
class AssinaturaAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "ss_nome",
        "ss_subdominio",
        "ss_cloudflare_id",
        "ss_codigo_licenca",
        "ss_status",
    )
    list_filter = ("ss_status",)
    search_fields = (
        "ss_nome",
        "ss_subdominio",
        "ss_cloudflare_id",
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
        "assinatura",
        "pl_numero_usuarios",
        "pl_numero_telas",
        "pl_integra_ifood",
        "pl_limite_integracoes_pedidos_ifood",
        "pl_valor_mensalidade",
        "pl_observacao",
    )
    list_filter = (
        "pl_tier",
        "ativo",
        "assinatura",
    )
    search_fields = (
        "pl_nome",
        "pl_observacao",
        "assinatura__ss_nome",
    )
    ordering = ("-id",)
    list_per_page = 25
