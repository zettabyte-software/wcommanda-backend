from django.urls import reverse

from rest_framework import status

import pytest

from apps.comandas.models import Comanda, ComandaItem, StatusComandaChoices


@pytest.fixture
def comanda(db, usuario, mesa):
    return Comanda.objects.create(cm_cliente="Cliente Teste", cm_mesa=mesa, cm_garcom=usuario)


@pytest.mark.django_db
def test_criar_comanda(api_client, usuario, mesa):
    api_client.force_authenticate(user=usuario)
    url = reverse("comanda-list")
    data = {"cm_cliente": "Cliente Teste", "cm_mesa": mesa.id, "cm_garcom": usuario.id}
    response = api_client.post(url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert Comanda.objects.count() == 1


@pytest.mark.django_db
def test_finalizar_comanda(api_client, usuario, comanda):
    api_client.force_authenticate(user=usuario)
    url = reverse("comanda-finalizar", args=[comanda.id])
    response = api_client.post(url, {}, format="json")
    assert response.status_code == status.HTTP_200_OK
    comanda.refresh_from_db()
    assert comanda.cm_status == StatusComandaChoices.FINALIZADA


@pytest.mark.django_db
def test_cancelar_comanda(api_client, usuario, comanda):
    api_client.force_authenticate(user=usuario)
    url = reverse("comanda-cancelar", args=[comanda.id])
    response = api_client.post(url, {}, format="json")
    assert response.status_code == status.HTTP_200_OK
    comanda.refresh_from_db()
    assert comanda.cm_status == StatusComandaChoices.CANCELADA


@pytest.mark.django_db
def test_visualizar_comanda(api_client, usuario, comanda, produto):
    api_client.force_authenticate(user=usuario)
    comanda_item = ComandaItem.objects.create(
        ct_comanda=comanda, ct_produto=produto, ct_preco_unitario_produto=produto.pr_preco
    )
    url = reverse("comanda-visualizar", args=[comanda.id])
    response = api_client.get(url, format="json")
    assert response.status_code == status.HTTP_200_OK
    assert "cm_valor_total" in response.data
    assert "cm_itens" in response.data
    assert response.data["cm_valor_total"] == comanda_item.ct_preco_unitario_produto
    assert response.data["cm_itens"][0]["ct_produto"] == produto.id
    assert response.data["cm_itens"][0]["ct_preco_unitario_produto"] == produto.pr_preco
