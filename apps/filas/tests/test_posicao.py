import pytest

from apps.filas.models import Fila


@pytest.fixture
def fila_factory(db):
    def create_fila(ff_posicao, ff_cliente="Cliente", ff_telefone="12345678901", ff_observacao=""):
        return Fila.objects.create(
            ff_posicao=ff_posicao,
            ff_cliente=ff_cliente,
            ff_telefone=ff_telefone,
            ff_observacao=ff_observacao,
        )

    return create_fila


@pytest.mark.django_db
def test_receber_pessoas(fila_factory):
    fila_factory(ff_posicao=1)
    fila_factory(ff_posicao=2)
    fila_factory(ff_posicao=3)

    Fila.receber_pessoas(1, 3)

    filas_restantes = list(Fila.objects.order_by("ff_posicao").values_list("ff_posicao", flat=True))
    assert filas_restantes == [1]


@pytest.mark.django_db
def test_receber_pessoas_sem_resultado():
    with pytest.raises(ValueError, match="Nenhuma pessoa encontrada nas posições especificadas."):
        Fila.receber_pessoas(404)


@pytest.mark.django_db
def test_remover_pessoa(fila_factory):
    fila_1 = fila_factory(ff_posicao=1)
    fila_2 = fila_factory(ff_posicao=2)

    Fila.remover_pessoa(fila_1.id)

    filas_restantes = list(Fila.objects.order_by("ff_posicao").values_list("ff_posicao", flat=True))
    assert filas_restantes == [1]


@pytest.mark.django_db
def test_remover_pessoa_nao_existente():
    with pytest.raises(ValueError, match="Pessoa não encontrada"):
        Fila.remover_pessoa(9999)


@pytest.mark.django_db
def test_mudar_posicao_para_cima(fila_factory):
    primeiro = fila_factory(ff_posicao=1)
    segundo = fila_factory(ff_posicao=2)
    terceiro = fila_factory(ff_posicao=3)

    Fila.mudar_posicao(terceiro.pk, 1)

    # filas = Fila.objects.order_by("ff_posicao").values_list("id", "ff_posicao", flat=True)

    primeiro.refresh_from_db()
    segundo.refresh_from_db()
    terceiro.refresh_from_db()

    assert primeiro.ff_posicao == 2
    assert segundo.ff_posicao == 3
    assert terceiro.ff_posicao == 1


@pytest.mark.django_db
def test_mudar_posicao_para_baixo(fila_factory):
    primeiro = fila_factory(ff_posicao=1)
    segundo = fila_factory(ff_posicao=2)
    terceiro = fila_factory(ff_posicao=3)

    Fila.mudar_posicao(primeiro.pk, 3)

    # filas = Fila.objects.order_by("ff_posicao").values_list("id", "ff_posicao", flat=True)
    primeiro.refresh_from_db()
    segundo.refresh_from_db()
    terceiro.refresh_from_db()

    assert primeiro.ff_posicao == 3
    assert segundo.ff_posicao == 1
    assert terceiro.ff_posicao == 2


@pytest.mark.django_db
def test_mudar_posicao_invalida(fila_factory):
    fila = fila_factory(ff_posicao=1)

    with pytest.raises(ValueError, match="Nova posição fora do intervalo permitido."):
        Fila.mudar_posicao(fila.id, 0)

    with pytest.raises(ValueError, match="Nova posição fora do intervalo permitido."):
        Fila.mudar_posicao(fila.id, 10)


@pytest.mark.django_db
def test_mudar_posicao_mesma_posicao(fila_factory):
    fila = fila_factory(ff_posicao=1)
    with pytest.raises(ValueError, match="As posições não podem ser as mesmas"):
        Fila.mudar_posicao(fila.id, 1)
