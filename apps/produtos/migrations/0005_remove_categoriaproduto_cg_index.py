# Generated by Django 5.1.3 on 2024-12-13 23:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('produtos', '0004_categoriaproduto_cg_index_produto_pr_organico_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='categoriaproduto',
            name='cg_index',
        ),
    ]