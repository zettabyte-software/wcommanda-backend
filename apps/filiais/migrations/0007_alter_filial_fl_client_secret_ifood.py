# Generated by Django 5.1.5 on 2025-04-21 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('filiais', '0006_filial_fl_client_id_ifood_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filial',
            name='fl_client_secret_ifood',
            field=models.CharField(blank=True, default='', max_length=300, verbose_name='clientId do iFood'),
        ),
    ]
