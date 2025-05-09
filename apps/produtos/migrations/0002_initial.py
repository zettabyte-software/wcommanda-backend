# Generated by Django 5.1.5 on 2025-01-31 19:36

import django.db.models.deletion
import django_multitenant.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('assinaturas', '0003_initial'),
        ('filiais', '0002_initial'),
        ('produtos', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='categoriaproduto',
            name='owner',
            field=django_multitenant.fields.TenantForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='owner'),
        ),
        migrations.AddField(
            model_name='complementoproduto',
            name='assinatura',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='assinaturas.assinatura', verbose_name='tenant'),
        ),
        migrations.AddField(
            model_name='complementoproduto',
            name='filial',
            field=django_multitenant.fields.TenantForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='filiais.filial', verbose_name='filial'),
        ),
        migrations.AddField(
            model_name='complementoproduto',
            name='owner',
            field=django_multitenant.fields.TenantForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='owner'),
        ),
        migrations.AddField(
            model_name='grupocomplementoproduto',
            name='assinatura',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='assinaturas.assinatura', verbose_name='tenant'),
        ),
        migrations.AddField(
            model_name='grupocomplementoproduto',
            name='filial',
            field=django_multitenant.fields.TenantForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='filiais.filial', verbose_name='filial'),
        ),
        migrations.AddField(
            model_name='grupocomplementoproduto',
            name='owner',
            field=django_multitenant.fields.TenantForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='owner'),
        ),
        migrations.AddField(
            model_name='complementoproduto',
            name='pc_grupo_complemento',
            field=django_multitenant.fields.TenantForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='complementos', to='produtos.grupocomplementoproduto', verbose_name='grupo de complemento'),
        ),
        migrations.AddField(
            model_name='produto',
            name='assinatura',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='assinaturas.assinatura', verbose_name='tenant'),
        ),
        migrations.AddField(
            model_name='produto',
            name='filial',
            field=django_multitenant.fields.TenantForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='filiais.filial', verbose_name='filial'),
        ),
        migrations.AddField(
            model_name='produto',
            name='owner',
            field=django_multitenant.fields.TenantForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='owner'),
        ),
        migrations.AddField(
            model_name='produto',
            name='pr_categoria',
            field=django_multitenant.fields.TenantForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='produtos.categoriaproduto', verbose_name='categoria'),
        ),
        migrations.AddField(
            model_name='produto',
            name='pr_grupo_complementos',
            field=django_multitenant.fields.TenantForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='produtos', to='produtos.grupocomplementoproduto', verbose_name='grupo de complementos'),
        ),
    ]
