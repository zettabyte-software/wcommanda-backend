# Generated by Django 5.1.3 on 2024-11-14 20:09

import django.db.models.deletion
import django_multitenant.fields
from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('estoque', '0003_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='movimentacaoestoque',
            name='owner',
            field=django_multitenant.fields.TenantForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='owner'),
        ),
    ]
