from django.contrib import admin

from .models import CategoriaProduto, Produto


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ("id", "pr_nome", "pr_descricao", "pr_preco", "pr_categoria")
    list_filter = ("pr_nome", "pr_descricao", "pr_preco", "pr_categoria")
    search_fields = ("pr_nome", "pr_descricao", "pr_preco", "pr_categoria")
    ordering = ("-id",)


@admin.register(CategoriaProduto)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("cg_nome", "cg_descricao")
    list_filter = ("cg_nome", "cg_descricao")
    search_fields = ("cg_nome", "cg_descricao")
    ordering = ("data_criacao", "cg_nome", "cg_descricao")

