# Generated by Django 5.1.5 on 2025-01-31 19:36

import apps.users.models
import django.db.models.deletion
import django.utils.timezone
import django_lifecycle.mixins
import django_multitenant.fields
import django_multitenant.mixins
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('assinaturas', '0002_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
        ('filiais', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('codigo', models.PositiveBigIntegerField(default=1, editable=False, verbose_name='código')),
                ('data_criacao', models.DateField(auto_now_add=True, verbose_name='data de criação')),
                ('hora_criacao', models.TimeField(auto_now_add=True, verbose_name='hora de criação')),
                ('data_ultima_alteracao', models.DateField(auto_now=True, verbose_name='data da última alteração')),
                ('hora_ultima_alteracao', models.TimeField(auto_now=True, verbose_name='hora da última alteração')),
                ('status', models.PositiveSmallIntegerField(choices=[(1, 'Pendente'), (2, 'Aceito'), (3, 'Recusado')], default=1, verbose_name='status')),
                ('first_name', models.CharField(max_length=30, verbose_name='nome')),
                ('last_name', models.CharField(max_length=60, verbose_name='sobrenome')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email')),
                ('is_waiter', models.BooleanField(default=False, verbose_name='é garçom')),
                ('is_screen', models.BooleanField(default=False, verbose_name='é usuário tela')),
                ('assinatura', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='assinaturas.assinatura', verbose_name='tenant')),
                ('filial', django_multitenant.fields.TenantForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='filiais.filial', verbose_name='filial')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Usuário',
                'verbose_name_plural': 'Usuários',
                'db_table': 'usuario',
                'ordering': ['-id'],
            },
            bases=(django_multitenant.mixins.TenantModelMixin, django_lifecycle.mixins.LifecycleModelMixin, models.Model),
            managers=[
                ('objects', apps.users.models.MultitenantUsuarioManager()),
                ('all_objects', apps.users.models.UsuarioManager()),
            ],
        ),
    ]
