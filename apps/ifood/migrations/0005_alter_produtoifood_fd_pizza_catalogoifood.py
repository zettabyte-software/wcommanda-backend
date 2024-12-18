# Generated by Django 5.1.3 on 2024-12-17 00:23

import django.db.models.deletion
import django.db.models.manager
import django_multitenant.fields
import django_multitenant.mixins
import django_multitenant.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('filiais', '0007_alter_filial_fl_catalog_id_and_more'),
        ('ifood', '0004_remove_categoriaifood_cd_filial'),
        ('tenants', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='produtoifood',
            name='fd_pizza',
            field=models.BooleanField(default=False, verbose_name='é pizza'),
        ),
        migrations.CreateModel(
            name='CatalogoIfood',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ativo', models.BooleanField(default=True, verbose_name='ativo')),
                ('codigo', models.PositiveBigIntegerField(default=1, editable=False, verbose_name='código')),
                ('data_criacao', models.DateField(auto_now_add=True, verbose_name='data de criação')),
                ('hora_criacao', models.TimeField(auto_now_add=True, verbose_name='hora de criação')),
                ('data_ultima_alteracao', models.DateField(auto_now=True, verbose_name='data da última alteração')),
                ('hora_ultima_alteracao', models.TimeField(auto_now=True, verbose_name='hora da última alteração')),
                ('cc_ifood_id', models.UUIDField(null=True, verbose_name='id do iFood')),
                ('ambiente', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='tenants.ambiente', verbose_name='tenant')),
                ('filial', django_multitenant.fields.TenantForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='filiais.filial', verbose_name='filial')),
                ('owner', django_multitenant.fields.TenantForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='owner')),
            ],
            options={
                'verbose_name': 'Catálogo do iFood',
                'verbose_name_plural': 'Catálogos do iFood',
                'db_table': 'catalogo_ifood',
                'ordering': ['-id'],
            },
            bases=(django_multitenant.mixins.TenantModelMixin, models.Model),
            managers=[
                ('all_objects', django.db.models.manager.Manager()),
                ('objects', django_multitenant.models.TenantManager()),
            ],
        ),
    ]