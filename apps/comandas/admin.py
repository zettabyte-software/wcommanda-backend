from django.contrib import admin

from .models import Comanda, ComandaItem


@admin.register(Comanda)
class ComandaAdmin(admin.ModelAdmin):
    list_display = ("cm_mesa", "cm_cliente")
    list_filter = ("cm_mesa", "cm_cliente")
    search_fields = ("cm_mesa", "garcom", "cm_cliente")
    ordering = ("data_criacao", "cm_mesa")


@admin.register(ComandaItem)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("ct_comanda", "ct_produto")
    list_filter = ("ct_comanda", "ct_produto")
    search_fields = ("ct_comanda", "ct_produto")
    ordering = ("ct_comanda", "ct_produto")
