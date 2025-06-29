import logging
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.hashers import make_password
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from django_multitenant.utils import set_current_tenant

from apps.filiais.models import Filial
from apps.system.assinaturas.models import Assinatura, Plano, StatusChoices, TierChoices
from apps.system.core.records import DefaultRecordsManger
from apps.users.models import StatusSolicitacao, Usuario
from lib.cloudflare.dns import criar_subdominio

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Cria uma nova assinatura com todos os dados relacionados"

    def add_arguments(self, parser):
        parser.add_argument(
            "--interactive",
            action="store_true",
            help="Modo interativo para inserção de dados",
        )

        # Argumentos para modo não-interativo
        parser.add_argument("--subdominio", type=str, help="Subdomínio da assinatura")
        parser.add_argument("--nome-assinatura", type=str, help="Nome da assinatura")
        parser.add_argument("--nome-plano", type=str, help="Nome do plano")
        parser.add_argument(
            "--tier", type=int, choices=[choice[0] for choice in TierChoices.choices], help="Tier do plano"
        )
        parser.add_argument("--numero-usuarios", type=int, help="Número de usuários")
        parser.add_argument("--integra-ifood", action="store_true", help="Integra com iFood")
        parser.add_argument("--limite-ifood", type=int, help="Limite de integrações iFood")
        parser.add_argument("--valor-mensalidade", type=float, help="Valor da mensalidade")
        parser.add_argument("--observacao", type=str, default="", help="Observação do plano")
        parser.add_argument("--email", type=str, help="Email do usuário")
        parser.add_argument("--password", type=str, help="Senha do usuário")
        parser.add_argument("--first-name", type=str, help="Primeiro nome")
        parser.add_argument("--last-name", type=str, help="Último nome")

    def handle(self, *args, **options):
        try:
            if options["interactive"]:
                data = self._get_interactive_data()
            else:
                data = self._get_arguments_data(options)

            # Criar assinatura
            self.stdout.write("Criando assinatura...")
            response_cloudflare = self._criar_cloudflare_subdomain(data["subdominio"])

            # Criar plano
            self.stdout.write("Criando plano...")
            plano = Plano.objects.create(
                pl_nome=data["nome_plano"],
                pl_tier=data["tier"],
                pl_numero_usuarios=data["numero_usuarios"],
                pl_integra_ifood=data["integra_ifood"],
                pl_limite_integracoes_pedidos_ifood=data["limite_ifood"],
                pl_valor_mensalidade=data["valor_mensalidade"],
                pl_observacao=data["observacao"],
            )

            assinatura = Assinatura.objects.create(
                ss_subdominio=data["subdominio"],
                ss_nome=data["nome_assinatura"],
                ss_cloudflare_id=response_cloudflare["result"]["id"],
                ss_status=StatusChoices.ULTRA,
                ss_plano=plano,
            )

            # Definir tenant atual
            set_current_tenant(assinatura)

            # Criar filial
            self.stdout.write("Criando filial...")
            filial = Filial.objects.create(fl_nome=f"{data['nome_assinatura']} - Principal", assinatura=assinatura)

            # Criar usuário
            self.stdout.write("Criando usuário...")
            usuario = Usuario.objects.create(
                status=StatusSolicitacao.ACEITO,
                email=data["email"],
                password=make_password(data["password"]),
                first_name=data["first_name"],
                last_name=data["last_name"],
                filial=filial,
                assinatura=assinatura,
            )

            # Aplicar registros padrão
            self.stdout.write("Aplicando registros padrão...")
            DefaultRecordsManger().apply_updates()

            self.stdout.write(
                self.style.SUCCESS(
                    f'Assinatura "{data["nome_assinatura"]}" criada com sucesso!\n'
                    f"Subdomínio: {data['subdominio']}\n"
                    f"Cloudflare ID: {response_cloudflare}\n"
                    f"Usuário: {data['email']}"
                )
            )

        except Exception as e:
            logger.error("Erro ao criar assinatura: %s", str(e))
            raise CommandError(f"Erro ao criar assinatura: {str(e)}")

    def _get_interactive_data(self):
        """Coleta dados do usuário de forma interativa"""
        data = {}

        # Dados da assinatura
        data["subdominio"] = self._input_with_validation("Subdomínio da assinatura: ", self._validate_subdomain)

        data["nome_assinatura"] = self._input_with_validation(
            "Nome da assinatura: ", lambda x: len(x.strip()) > 0, "Nome da assinatura não pode estar vazio"
        )

        # Dados do plano
        data["nome_plano"] = self._input_with_validation(
            "Nome do plano: ", lambda x: len(x.strip()) > 0, "Nome do plano não pode estar vazio"
        )

        # Mostrar opções de tier
        self.stdout.write("\nOpções de Tier:")
        for choice in TierChoices.choices:
            self.stdout.write(f"  {choice[0]} - {choice[1]}")

        data["tier"] = self._input_with_validation(
            "Tier do plano: ",
            lambda x: x.isdigit() and int(x) in [choice[0] for choice in TierChoices.choices],
            "Tier inválido",
            transform=int,
        )

        data["numero_usuarios"] = self._input_with_validation(
            "Número de usuários: ",
            lambda x: x.isdigit() and int(x) > 0,
            "Deve ser um número inteiro positivo",
            transform=int,
        )

        integra_ifood = input("Integra com iFood? (s/n): ").lower().strip()
        data["integra_ifood"] = integra_ifood in ["s", "sim", "y", "yes"]

        if data["integra_ifood"]:
            data["limite_ifood"] = self._input_with_validation(
                "Limite de integrações iFood: ",
                lambda x: x.isdigit() and int(x) >= 0,
                "Deve ser um número inteiro não negativo",
                transform=int,
            )
        else:
            data["limite_ifood"] = 0

        data["valor_mensalidade"] = self._input_with_validation(
            "Valor da mensalidade: ",
            lambda x: self._is_valid_decimal(x),
            "Deve ser um número decimal válido",
            transform=float,
        )

        data["observacao"] = input("Observação (opcional): ").strip()

        # Dados do usuário
        self.stdout.write("\n--- Dados do Usuário ---")

        data["email"] = self._input_with_validation("Email: ", self._validate_email)

        data["password"] = self._input_with_validation(
            "Senha: ", lambda x: len(x) >= 6, "Senha deve ter pelo menos 6 caracteres"
        )

        data["first_name"] = self._input_with_validation(
            "Primeiro nome: ", lambda x: len(x.strip()) > 0, "Primeiro nome não pode estar vazio"
        )

        data["last_name"] = self._input_with_validation(
            "Último nome: ", lambda x: len(x.strip()) > 0, "Último nome não pode estar vazio"
        )

        return data

    def _get_arguments_data(self, options):
        """Valida e organiza dados dos argumentos da linha de comando"""
        required_fields = [
            "subdominio",
            "nome_assinatura",
            "nome_plano",
            "tier",
            "numero_usuarios",
            "limite_ifood",
            "valor_mensalidade",
            "email",
            "password",
            "first_name",
            "last_name",
        ]

        for field in required_fields:
            field_key = field.replace("_", "-")
            if not options.get(field_key.replace("-", "_")):
                raise CommandError(f"Campo obrigatório: --{field_key}")

        # Validações
        if not self._validate_subdomain(options["subdominio"]):
            raise CommandError("Subdomínio inválido")

        if not self._validate_email(options["email"]):
            raise CommandError("Email inválido")

        if len(options["password"]) < 6:
            raise CommandError("Senha deve ter pelo menos 6 caracteres")

        return {
            "subdominio": options["subdominio"],
            "nome_assinatura": options["nome_assinatura"],
            "nome_plano": options["nome_plano"],
            "tier": options["tier"],
            "numero_usuarios": options["numero_usuarios"],
            "integra_ifood": options["integra_ifood"],
            "limite_ifood": options["limite_ifood"] or 0,
            "valor_mensalidade": options["valor_mensalidade"],
            "observacao": options["observacao"] or "",
            "email": options["email"],
            "password": options["password"],
            "first_name": options["first_name"],
            "last_name": options["last_name"],
        }

    def _input_with_validation(self, prompt, validator, error_msg="Valor inválido", transform=None):
        """Solicita input com validação"""
        while True:
            value = input(prompt).strip()
            if validator(value):
                return transform(value) if transform else value
            self.stdout.write(self.style.ERROR(error_msg))

    def _validate_subdomain(self, subdomain):
        """Valida formato do subdomínio"""
        if not subdomain:
            return False

        # Verifica se contém apenas letras, números e hífens
        import re

        if not re.match(r"^[a-zA-Z0-9-]+$", subdomain):
            return False

        # Verifica se não começa ou termina com hífen
        if subdomain.startswith("-") or subdomain.endswith("-"):
            return False

        # Verifica se já existe
        if Assinatura.objects.filter(ss_subdominio=subdomain).exists():
            self.stdout.write(self.style.ERROR("Subdomínio já existe"))
            return False

        return True

    def _validate_email(self, email):
        """Valida formato do email"""
        validator = EmailValidator()
        try:
            validator(email)
            # Verifica se já existe
            if Usuario.objects.filter(email=email).exists():
                self.stdout.write(self.style.ERROR("Email já existe"))
                return False
            return True
        except ValidationError:
            return False

    def _is_valid_decimal(self, value):
        """Verifica se é um número decimal válido"""
        try:
            float(value)
            return float(value) >= 0
        except ValueError:
            return False

    def _criar_cloudflare_subdomain(self, subdomain):
        """Cria subdomínio no Cloudflare e retorna o ID"""
        try:
            self.stdout.write(f"Criando subdomínio '{subdomain}' no Cloudflare...")
            cloudflare_id = criar_subdominio(subdomain)
            self.stdout.write(self.style.SUCCESS(f"Subdomínio criado com ID: {cloudflare_id}"))
            return cloudflare_id
        except Exception as e:
            raise CommandError(f"Erro ao criar subdomínio no Cloudflare: {str(e)}")
