# Generated by Django 5.1.3 on 2024-12-14 02:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produtos', '0005_remove_categoriaproduto_cg_index'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categoriaproduto',
            name='cg_descricao',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='descrição'),
        ),
    ]