# Generated by Django 5.1.5 on 2025-01-31 19:36

import django.db.models.deletion
import django_multitenant.fields
from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('filiais', '0002_initial'),
        ('garcons', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='comissaogarcom',
            name='cg_garcom',
            field=django_multitenant.fields.TenantForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='comissoes', to=settings.AUTH_USER_MODEL, verbose_name='garçom'),
        ),
        migrations.AddField(
            model_name='comissaogarcom',
            name='filial',
            field=django_multitenant.fields.TenantForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='filiais.filial', verbose_name='filial'),
        ),
        migrations.AddField(
            model_name='comissaogarcom',
            name='owner',
            field=django_multitenant.fields.TenantForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='owner'),
        ),
    ]
