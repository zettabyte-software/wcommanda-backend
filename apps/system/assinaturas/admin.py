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
        "ss_integracoes_ifood",
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
        "pl_assinatura",
        "pl_numero_usuarios",
        "pl_limite_integracoes_ifood",
        "pl_valor_mensalidade",
        "pl_observacao",
    )
    list_filter = (
        "pl_tier",
        "ativo",
        "pl_assinatura",
    )
    search_fields = (
        "pl_nome",
        "pl_observacao",
        "pl_assinatura__ss_nome",
    )
    ordering = ("-id",)
    list_per_page = 25
