from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand

from django_multitenant.utils import set_current_tenant

from apps.system.core.records import DefaultRecordsManger
from apps.system.tenants.models import Ambiente
from apps.users.models import Usuario


class Command(BaseCommand):
    help = "Cria um tenant e um usuário"

    def add_arguments(self, parser):
        # Argumentos do Ambiente
        parser.add_argument("--mb_nome", type=str, required=True, help="Nome do Ambiente")
        parser.add_argument("--mb_subdominio", type=str, required=True, help="Subdomínio do Ambiente")

        # Argumentos do Usuário
        parser.add_argument("--first_name", type=str, required=True, help="Nome do usuário")
        parser.add_argument("--last_name", type=str, required=True, help="Sobrenome do usuário")
        parser.add_argument("--password", type=str, required=True, help="Senha para o usuário")
        parser.add_argument("--email", type=str, required=True, help="Email do usuário")
        parser.add_argument("--is_waiter", type=bool, default=False, help="O usuário é um garçom")
        parser.add_argument("--is_screen", type=bool, default=False, help="O usuário possui tela")

    def handle(self, *args, **options):
        ambiente = Ambiente.objects.create(mb_nome=options["mb_nome"], mb_subdominio=options["mb_subdominio"])

        self.stdout.write(self.style.SUCCESS("Ambiente criado com sucesso!"))

        Usuario.objects.create(
            first_name=options["first_name"],
            last_name=options["last_name"],
            password=make_password(options["password"]),
            email=options["email"],
            is_waiter=options["is_waiter"],
            is_screen=options["is_screen"],
            ambiente=ambiente,
        )

        self.stdout.write(self.style.SUCCESS("Usuário criado com sucesso!"))

        set_current_tenant(ambiente)

        DefaultRecordsManger().apply_updates()

        self.stdout.write(self.style.SUCCESS("Configurações criadas com sucesso!"))
