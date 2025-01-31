import logging
import os
from shutil import rmtree

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import connection

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Reseta o histórico de migrações do banco de dados do sistema"

    def handle(self, *args, **options):
        self.recriar_migracoes()

    def recriar_migracoes(self):
        self.deletar_migracoes()
        self.criar_pastas_migracao()

        if settings.DATABASES["default"]["ENGINE"] == "django.db.backends.sqlite3":
            os.remove("db.sqlite3")

        self.aplicar_migracoes()

    def deletar_migracoes(self):
        for app in settings.WCOMMANDA_APPS:
            app_path = app.replace(".", "/")
            migration_path = app_path + "/migrations"

            if os.path.exists(migration_path):
                rmtree(migration_path)

    def criar_pastas_migracao(self):
        for app in settings.WCOMMANDA_APPS:
            app_path = app.replace(".", "/")
            migration_path = app_path + "/migrations"
            init_path = migration_path + "/__init__.py"

            if not os.path.exists(init_path):
                os.makedirs(migration_path)

            if not os.path.exists(init_path):
                with open(init_path, "x") as f:
                    f.close()

    def clean_django_migrations_table(self):
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM django_migrations")
        rows = cursor.fetchall()

        for row in rows:
            id, app, name, _ = row
            system_apps = ("admin", "auth", "contenttypes", "sessions", "accounts", "authtoken")
            if app not in system_apps and "initial" not in name:
                cursor.execute("DELETE FROM django_migrations WHERE id = %s", [id])

    def aplicar_migracoes(self):
        try:
            self.clean_django_migrations_table()
        except Exception:
            pass

        call_command("makemigrations")
        call_command("migrate")
