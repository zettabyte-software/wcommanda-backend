import json

from rest_framework import status

import pytest

from apps.produtos.models import Produto, TiposChoices


@pytest.fixture
def produtos(assinatura):
    json_configuracoes = json.load(open("data/mock/produtos.json"))
    for dados in json_configuracoes:
        Produto.objects.create(
            pr_path_imagem="undefined",
            pr_id_back_blaze="undefined",
            assinatura=assinatura,
            **dados,
        )


@pytest.mark.django_db
def test_list_produtos(api_client, produtos):
    response = api_client.get("/api/v1/produtos/")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data["resultados"]) == Produto.objects.all().count()

    for produto in response.data:
        assert "pr_path_imagem" not in produto
        assert "pr_id_back_blaze" not in produto


@pytest.mark.django_db
def test_retrieve_produto(api_client, produto):
    response = api_client.get(f"/api/v1/produtos/{produto.id}/")

    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == produto.id
    assert "pr_path_imagem" not in response.data
    assert "pr_id_back_blaze" not in response.data


@pytest.mark.django_db
def test_create_produto(api_client):
    data = {
        "pr_nome": "Test Product",
        "pr_descricao": "Test Description",
        "pr_tipo": TiposChoices.CONSUMIVEL,
        "pr_valor": 10,
        "pr_codigo_cardapio": "910",
        "pr_path_imagem": "should_not_be_saved.jpg",
        "pr_id_back_blaze": "should_not_be_saved",
    }

    response = api_client.post("/api/v1/produtos/", data)

    assert response.status_code == status.HTTP_201_CREATED
    assert "pr_path_imagem" not in response.data
    assert "pr_id_back_blaze" not in response.data

    produto = Produto.objects.get(id=response.data["id"])
    assert produto.pr_path_imagem == ""
    assert produto.pr_id_back_blaze == ""


@pytest.mark.django_db
def test_partial_update_produto(api_client, produto):
    data = {
        "pr_nome": "Updated Name",
        "pr_path_imagem": "should_not_update.jpg",
        "pr_id_back_blaze": "should_not_update",
    }

    response = api_client.patch(f"/api/v1/produtos/{produto.id}/", data)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["pr_nome"] == "Updated Name"
    assert "pr_path_imagem" not in response.data
    assert "pr_id_back_blaze" not in response.data

    produto.refresh_from_db()
    assert produto.pr_nome == "Updated Name"
    assert produto.pr_path_imagem == "undefined"
    assert produto.pr_id_back_blaze == "undefined"
