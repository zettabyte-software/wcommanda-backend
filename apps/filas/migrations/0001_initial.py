# Generated by Django 5.1.3 on 2024-12-17 00:23

import django.db.models.deletion
import django.db.models.manager
import django_multitenant.fields
import django_multitenant.mixins
import django_multitenant.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('filiais', '0007_alter_filial_fl_catalog_id_and_more'),
        ('tenants', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Fila',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ativo', models.BooleanField(default=True, verbose_name='ativo')),
                ('codigo', models.PositiveBigIntegerField(default=1, editable=False, verbose_name='código')),
                ('data_criacao', models.DateField(auto_now_add=True, verbose_name='data de criação')),
                ('hora_criacao', models.TimeField(auto_now_add=True, verbose_name='hora de criação')),
                ('data_ultima_alteracao', models.DateField(auto_now=True, verbose_name='data da última alteração')),
                ('hora_ultima_alteracao', models.TimeField(auto_now=True, verbose_name='hora da última alteração')),
                ('ff_posicao', models.PositiveSmallIntegerField(default=1, verbose_name='posição')),
                ('ff_cliente', models.CharField(max_length=40, verbose_name='cliente')),
                ('ff_telefone', models.CharField(max_length=11, verbose_name='cliente')),
                ('ff_observacao', models.CharField(max_length=60, verbose_name='cliente')),
                ('ambiente', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='tenants.ambiente', verbose_name='tenant')),
                ('filial', django_multitenant.fields.TenantForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='filiais.filial', verbose_name='filial')),
                ('owner', django_multitenant.fields.TenantForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='owner')),
            ],
            options={
                'verbose_name': 'Fila',
                'verbose_name_plural': 'Filas',
                'db_table': 'fila',
                'ordering': ['-id'],
            },
            bases=(django_multitenant.mixins.TenantModelMixin, models.Model),
            managers=[
                ('all_objects', django.db.models.manager.Manager()),
                ('objects', django_multitenant.models.TenantManager()),
            ],
        ),
    ]