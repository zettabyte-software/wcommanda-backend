# Generated by Django 5.1.5 on 2025-02-04 14:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('filiais', '0002_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='filial',
            old_name='fl_catalogo_grupo_id',
            new_name='fl_catalog_grupo_id',
        ),
        migrations.RenameField(
            model_name='filial',
            old_name='fl_catalogo_id',
            new_name='fl_catalog_id',
        ),
    ]
