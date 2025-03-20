from django.urls import reverse

from rest_framework import status

import pytest
from faker import Faker

from apps.clientes.models import Cliente

faker = Faker()


@pytest.mark.django_db
def test_criar_cliente(api_client):
    """Testa a criação de um novo cliente."""
    endpoint = reverse("cliente-list")

    data = {
        "cl_nome": faker.first_name(),
        "cl_sobrenome": faker.last_name(),
        "cl_nascimento": faker.date_of_birth(minimum_age=18, maximum_age=90).isoformat(),
        "cl_celular": faker.msisdn()[:11],
        "cl_telefone": faker.msisdn()[:10],
        "cl_email": faker.email(),
        "cl_cep": faker.postcode(),
        "cl_estado": 1,  # Supondo que o estado tenha um valor válido
        "cl_cidade": faker.city(),
        "cl_bairro": faker.street_name(),
        "cl_rua": faker.street_address(),
        "cl_numero": str(faker.random_int(min=1, max=9999)),
        "cl_complemento": faker.sentence(nb_words=4),
    }

    response = api_client.post(endpoint, data, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert Cliente.objects.filter(cl_email=data["cl_email"]).exists()


@pytest.mark.django_db
def test_listar_clientes(api_client):
    """Testa a listagem de clientes."""
    endpoint = reverse("cliente-list")

    Cliente.objects.create(
        cl_nome=faker.first_name(),
        cl_sobrenome=faker.last_name(),
        cl_email=faker.email(),
    )

    response = api_client.get(endpoint)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) > 0


@pytest.mark.django_db
def test_obter_cliente(api_client):
    """Testa obter detalhes de um cliente específico."""
    cliente = Cliente.objects.create(
        cl_nome=faker.first_name(),
        cl_sobrenome=faker.last_name(),
        cl_email=faker.email(),
    )

    endpoint = reverse("cliente-detail", args=[cliente.id])
    response = api_client.get(endpoint)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["cl_email"] == cliente.cl_email


@pytest.mark.django_db
def test_atualizar_cliente(api_client):
    """Testa a atualização de um cliente."""
    cliente = Cliente.objects.create(
        cl_nome=faker.first_name(),
        cl_sobrenome=faker.last_name(),
        cl_email=faker.email(),
    )

    endpoint = reverse("cliente-detail", args=[cliente.id])
    novo_nome = faker.first_name()
    response = api_client.patch(endpoint, {"cl_nome": novo_nome}, format="json")

    assert response.status_code == status.HTTP_200_OK
    cliente.refresh_from_db()
    assert cliente.cl_nome == novo_nome


@pytest.mark.django_db
def test_excluir_cliente(api_client):
    """Testa a exclusão de um cliente."""
    cliente = Cliente.objects.create(
        cl_nome=faker.first_name(),
        cl_sobrenome=faker.last_name(),
        cl_email=faker.email(),
    )

    endpoint = reverse("cliente-detail", args=[cliente.id])
    response = api_client.delete(endpoint)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Cliente.objects.filter(id=cliente.id).exists()
