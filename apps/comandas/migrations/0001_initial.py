# Generated by Django 5.1.5 on 2025-01-31 19:36

import django.db.models.deletion
import django.db.models.manager
import django_lifecycle.mixins
import django_multitenant.mixins
import django_multitenant.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('assinaturas', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ComandaItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ativo', models.BooleanField(default=True, verbose_name='ativo')),
                ('codigo', models.PositiveBigIntegerField(default=1, editable=False, verbose_name='código')),
                ('data_criacao', models.DateField(auto_now_add=True, verbose_name='data de criação')),
                ('hora_criacao', models.TimeField(auto_now_add=True, verbose_name='hora de criação')),
                ('data_ultima_alteracao', models.DateField(auto_now=True, verbose_name='data da última alteração')),
                ('hora_ultima_alteracao', models.TimeField(auto_now=True, verbose_name='hora da última alteração')),
                ('ct_status', models.PositiveSmallIntegerField(choices=[(1, 'Aberto'), (2, 'Preparando'), (3, 'Pronto'), (4, 'Entregue'), (5, 'Cancelado')], default=1, verbose_name='status')),
                ('ct_pedido', models.PositiveSmallIntegerField(default=0, verbose_name='sequência')),
                ('ct_preco_unitario_produto', models.FloatField(default=0, verbose_name='preço unitário do produto')),
                ('ct_premio', models.BooleanField(default=False, verbose_name='é um prêmio')),
                ('ct_data_preparamento', models.DateField(null=True, verbose_name='data do preparamento')),
                ('ct_hora_preparamento', models.TimeField(null=True, verbose_name='hora do preparamento')),
                ('ct_data_finalizacao', models.DateField(null=True, verbose_name='data da finalização')),
                ('ct_hora_finalizacao', models.TimeField(null=True, verbose_name='hora da finalização')),
                ('ct_data_entregue', models.DateField(null=True, verbose_name='data da entrega ao cliente')),
                ('ct_hora_entregue', models.TimeField(null=True, verbose_name='hora da entrega ao cliente')),
                ('ct_observacao', models.CharField(blank=True, max_length=100, verbose_name='observação')),
            ],
            options={
                'verbose_name': 'Item da Comanda',
                'verbose_name_plural': 'Items da Comanda',
                'db_table': 'comanda_item',
                'ordering': ['-id'],
            },
            bases=(django_multitenant.mixins.TenantModelMixin, django_lifecycle.mixins.LifecycleModelMixin, models.Model),
            managers=[
                ('all_objects', django.db.models.manager.Manager()),
                ('objects', django_multitenant.models.TenantManager()),
            ],
        ),
        migrations.CreateModel(
            name='Comanda',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ativo', models.BooleanField(default=True, verbose_name='ativo')),
                ('codigo', models.PositiveBigIntegerField(default=1, editable=False, verbose_name='código')),
                ('data_criacao', models.DateField(auto_now_add=True, verbose_name='data de criação')),
                ('hora_criacao', models.TimeField(auto_now_add=True, verbose_name='hora de criação')),
                ('data_ultima_alteracao', models.DateField(auto_now=True, verbose_name='data da última alteração')),
                ('hora_ultima_alteracao', models.TimeField(auto_now=True, verbose_name='hora da última alteração')),
                ('cm_codigo', models.PositiveSmallIntegerField(default=1, editable=False, verbose_name='código')),
                ('cm_status', models.PositiveSmallIntegerField(choices=[(1, 'Aberta'), (2, 'Finalizada'), (3, 'Cancelada')], default=1, verbose_name='status')),
                ('cm_cliente', models.CharField(blank=True, max_length=30, verbose_name='cliente')),
                ('cm_forma_pagamento', models.PositiveSmallIntegerField(choices=[(1, 'Cartão de Crédito'), (2, 'Cartão de Débito'), (3, 'Dinheiro'), (4, 'PIX'), (99, 'Outro')], null=True, verbose_name='forma de pagamento')),
                ('cm_data_finalizacao', models.DateField(null=True, verbose_name='data da finalização')),
                ('cm_hora_finalizacao', models.TimeField(null=True, verbose_name='hora da finalização')),
                ('cm_data_cancelamento', models.DateField(null=True, verbose_name='data do cancelamento')),
                ('cm_hora_cancelamento', models.TimeField(null=True, verbose_name='hora do cancelamento')),
                ('cm_motivo_cancelamento', models.CharField(blank=True, max_length=50, verbose_name='motivo do cancelamento')),
                ('assinatura', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='assinaturas.assinatura', verbose_name='tenant')),
            ],
            options={
                'verbose_name': 'Comanda',
                'verbose_name_plural': 'Comandas',
                'db_table': 'comanda',
                'ordering': ['-id'],
            },
            bases=(django_multitenant.mixins.TenantModelMixin, django_lifecycle.mixins.LifecycleModelMixin, models.Model),
            managers=[
                ('all_objects', django.db.models.manager.Manager()),
                ('objects', django_multitenant.models.TenantManager()),
            ],
        ),
    ]
