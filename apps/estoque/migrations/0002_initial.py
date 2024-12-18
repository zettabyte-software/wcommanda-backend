# Generated by Django 5.1.3 on 2024-11-14 20:09

import django.db.models.deletion
import django_multitenant.fields
from django.db import migrations


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('comandas', '0002_initial'),
        ('estoque', '0001_initial'),
        ('filiais', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='movimentacaoestoque',
            name='filial',
            field=django_multitenant.fields.TenantForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='filiais.filial', verbose_name='filial'),
        ),
        migrations.AddField(
            model_name='movimentacaoestoque',
            name='mv_comanda_item',
            field=django_multitenant.fields.TenantForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='movimentacoes', to='comandas.comandaitem', verbose_name='comanda item'),
        ),
    ]
