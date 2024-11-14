from rest_framework.test import APITestCase

from django_multitenant.utils import set_current_tenant

from apps.system.tenants.models import Ambiente


class BaseTestCase(APITestCase):
    def setUp(self):
        set_current_tenant(Ambiente.objects.create(mb_nome="Teste", mb_subdominio="teste"))
