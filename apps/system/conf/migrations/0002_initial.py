# Generated by Django 5.1.5 on 2025-01-31 19:36

import django.db.models.deletion
import django_multitenant.fields
from django.db import migrations


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('conf', '0001_initial'),
        ('filiais', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='configuracao',
            name='filial',
            field=django_multitenant.fields.TenantForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='filiais.filial', verbose_name='filial'),
        ),
    ]
