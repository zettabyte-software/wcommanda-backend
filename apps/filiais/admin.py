from django.contrib import admin
from .models import Filial


@admin.register(Filial)
class FilialAdmin(admin.ModelAdmin):
    pass
