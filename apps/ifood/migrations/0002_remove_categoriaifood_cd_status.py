# Generated by Django 5.1.3 on 2024-12-14 03:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ifood', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='categoriaifood',
            name='cd_status',
        ),
    ]