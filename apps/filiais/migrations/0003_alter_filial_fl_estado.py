# Generated by Django 5.1.3 on 2024-11-28 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('filiais', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filial',
            name='fl_estado',
            field=models.CharField(choices=[(0, 'Em branco'), (1, 'Rondônia'), (2, 'Acre'), (3, 'Amazonas'), (4, 'Roraima'), (5, 'Pará'), (6, 'Amapá'), (7, 'Tocantins'), (8, 'Maranhão'), (9, 'Piauí'), (10, 'Ceará'), (11, 'Rio Grande do Norte'), (12, 'Paraíba'), (13, 'Pernambuco'), (14, 'Alagoas'), (15, 'Sergipe'), (16, 'Bahia'), (17, 'Minas Gerais'), (18, 'Espírito Santo'), (19, 'Rio de Janeiro'), (20, 'São Paulo'), (21, 'Paraná'), (22, 'Santa Catarina'), (23, 'Rio Grande do Sul'), (24, 'Mato Grosso do Sul'), (25, 'Mato Grosso'), (26, 'Goiás'), (27, 'Distrito Federal'), (28, 'Exterior')], default=0, max_length=3, verbose_name='estado'),
        ),
    ]
