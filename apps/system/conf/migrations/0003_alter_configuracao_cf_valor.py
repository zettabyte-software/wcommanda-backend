# Generated by Django 5.1.3 on 2024-11-23 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conf', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='configuracao',
            name='cf_valor',
            field=models.CharField(max_length=150, verbose_name='valor'),
        ),
    ]
