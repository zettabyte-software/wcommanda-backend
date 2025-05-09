# Generated by Django 5.1.5 on 2025-01-31 19:36

import django.core.validators
import django.db.models.deletion
import django.db.models.manager
import django_lifecycle.mixins
import django_multitenant.fields
import django_multitenant.mixins
import django_multitenant.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('assinaturas', '0002_initial'),
        ('filiais', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ComplementoProduto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ativo', models.BooleanField(default=True, verbose_name='ativo')),
                ('codigo', models.PositiveBigIntegerField(default=1, editable=False, verbose_name='código')),
                ('data_criacao', models.DateField(auto_now_add=True, verbose_name='data de criação')),
                ('hora_criacao', models.TimeField(auto_now_add=True, verbose_name='hora de criação')),
                ('data_ultima_alteracao', models.DateField(auto_now=True, verbose_name='data da última alteração')),
                ('hora_ultima_alteracao', models.TimeField(auto_now=True, verbose_name='hora da última alteração')),
                ('pc_nome', models.CharField(max_length=40, verbose_name='nome')),
                ('pc_preco', models.FloatField(default=0, verbose_name='preço')),
                ('pc_quantidade_minima', models.FloatField(default=1, verbose_name='quantidade máxima')),
                ('pc_quantidade_maxima', models.FloatField(default=1, verbose_name='quantidade máxima')),
                ('pc_descricao', models.CharField(blank=True, max_length=50, verbose_name='descrição')),
                ('pc_obrigatorio', models.BooleanField(default=False, verbose_name='obrigatório')),
            ],
            options={
                'verbose_name': 'Complemento do Produto',
                'verbose_name_plural': 'Complementos dos Produtos',
                'db_table': 'complemento_produto',
                'ordering': ['-id'],
            },
            bases=(django_multitenant.mixins.TenantModelMixin, django_lifecycle.mixins.LifecycleModelMixin, models.Model),
            managers=[
                ('all_objects', django.db.models.manager.Manager()),
                ('objects', django_multitenant.models.TenantManager()),
            ],
        ),
        migrations.CreateModel(
            name='GrupoComplementoProduto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ativo', models.BooleanField(default=True, verbose_name='ativo')),
                ('codigo', models.PositiveBigIntegerField(default=1, editable=False, verbose_name='código')),
                ('data_criacao', models.DateField(auto_now_add=True, verbose_name='data de criação')),
                ('hora_criacao', models.TimeField(auto_now_add=True, verbose_name='hora de criação')),
                ('data_ultima_alteracao', models.DateField(auto_now=True, verbose_name='data da última alteração')),
                ('hora_ultima_alteracao', models.TimeField(auto_now=True, verbose_name='hora da última alteração')),
                ('gr_nome', models.CharField(max_length=30, verbose_name='nome')),
            ],
            options={
                'verbose_name': 'Grupo de Acréscimo do Produto',
                'verbose_name_plural': 'Grupos de Acréscimos dos Produtos',
                'db_table': 'grupo_complemento_produto',
                'ordering': ['-id'],
            },
            bases=(django_multitenant.mixins.TenantModelMixin, django_lifecycle.mixins.LifecycleModelMixin, models.Model),
            managers=[
                ('all_objects', django.db.models.manager.Manager()),
                ('objects', django_multitenant.models.TenantManager()),
            ],
        ),
        migrations.CreateModel(
            name='Produto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ativo', models.BooleanField(default=True, verbose_name='ativo')),
                ('codigo', models.PositiveBigIntegerField(default=1, editable=False, verbose_name='código')),
                ('data_criacao', models.DateField(auto_now_add=True, verbose_name='data de criação')),
                ('hora_criacao', models.TimeField(auto_now_add=True, verbose_name='hora de criação')),
                ('data_ultima_alteracao', models.DateField(auto_now=True, verbose_name='data da última alteração')),
                ('hora_ultima_alteracao', models.TimeField(auto_now=True, verbose_name='hora da última alteração')),
                ('pr_tipo', models.PositiveSmallIntegerField(choices=[(1, 'Preparável'), (2, 'Consumível')], default=2, verbose_name='tipo')),
                ('pr_nome', models.CharField(max_length=100, verbose_name='nome')),
                ('pr_codigo_cardapio', models.CharField(max_length=8, verbose_name='código do cardápio')),
                ('pr_preco', models.FloatField(default=0, verbose_name='preço')),
                ('pr_tempo_preparo', models.IntegerField(default=0, verbose_name='código')),
                ('pr_descricao', models.TextField(blank=True, default='', verbose_name='descrição')),
                ('pr_controla_estoque', models.BooleanField(default=False, verbose_name='controla estoque')),
                ('pr_status_padrao_comanda_item', models.PositiveSmallIntegerField(choices=[(1, 'Aberto'), (2, 'Preparando'), (3, 'Pronto'), (4, 'Entregue'), (5, 'Cancelado')], default=1, verbose_name='tipo')),
                ('pr_imagem', models.URLField(blank=True, default='', verbose_name='foto')),
                ('pr_vegano', models.BooleanField(default=False, verbose_name='vegano')),
                ('pr_vegetariano', models.BooleanField(default=False, verbose_name='vegetariano')),
                ('pr_organico', models.BooleanField(default=False, verbose_name='orgânico')),
                ('pr_sem_gluten', models.BooleanField(default=False, verbose_name='sem glúten')),
                ('pr_sem_acucar', models.BooleanField(default=False, verbose_name='sem açúcar')),
                ('pr_zero_lactose', models.BooleanField(default=False, verbose_name='zero lactose')),
                ('pr_serve_pessoas', models.PositiveSmallIntegerField(null=True, validators=[django.core.validators.MaxValueValidator(4)], verbose_name='n° de pessoas que a comida serve')),
                ('pr_unidade', models.PositiveSmallIntegerField(choices=[(1, 'Grama'), (2, 'Quilo'), (3, 'Mililitro'), (4, 'Litro'), (5, 'Unidade'), (6, 'Fatia'), (7, 'Porção'), (99, 'Outra')], null=True, verbose_name='tipo')),
                ('pr_quantidade', models.IntegerField(default=0, verbose_name='tipo')),
            ],
            options={
                'verbose_name': 'Produto',
                'verbose_name_plural': 'Produtos',
                'db_table': 'produto',
                'ordering': ['-id'],
            },
            bases=(django_multitenant.mixins.TenantModelMixin, django_lifecycle.mixins.LifecycleModelMixin, models.Model),
            managers=[
                ('all_objects', django.db.models.manager.Manager()),
                ('objects', django_multitenant.models.TenantManager()),
            ],
        ),
        migrations.CreateModel(
            name='CategoriaProduto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ativo', models.BooleanField(default=True, verbose_name='ativo')),
                ('codigo', models.PositiveBigIntegerField(default=1, editable=False, verbose_name='código')),
                ('data_criacao', models.DateField(auto_now_add=True, verbose_name='data de criação')),
                ('hora_criacao', models.TimeField(auto_now_add=True, verbose_name='hora de criação')),
                ('data_ultima_alteracao', models.DateField(auto_now=True, verbose_name='data da última alteração')),
                ('hora_ultima_alteracao', models.TimeField(auto_now=True, verbose_name='hora da última alteração')),
                ('cg_nome', models.CharField(max_length=30, verbose_name='nome')),
                ('cg_descricao', models.CharField(blank=True, default='', max_length=100, verbose_name='descrição')),
                ('assinatura', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='assinaturas.assinatura', verbose_name='tenant')),
                ('filial', django_multitenant.fields.TenantForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='filiais.filial', verbose_name='filial')),
            ],
            options={
                'verbose_name': 'Categoria',
                'verbose_name_plural': 'Categorias',
                'db_table': 'categoria_produto',
                'ordering': ['-id'],
            },
            bases=(django_multitenant.mixins.TenantModelMixin, django_lifecycle.mixins.LifecycleModelMixin, models.Model),
            managers=[
                ('all_objects', django.db.models.manager.Manager()),
                ('objects', django_multitenant.models.TenantManager()),
            ],
        ),
    ]
