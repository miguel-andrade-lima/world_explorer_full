import pytest

from backend import database
from backend.app import app


@pytest.fixture
def cliente(tmp_path, monkeypatch):
    # Usa um banco temporário para não alterar os favoritos reais.
    caminho_banco = tmp_path / "teste_paises.db"
    monkeypatch.setattr(database, "DATABASE_PATH", caminho_banco)

    database.criar_tabela()

    app.config["TESTING"] = True

    with app.test_client() as cliente:
        yield cliente


def criar_pais():
    return {
        "nome": "Brazil",
        "capital": "Brasília",
        "populacao": 214211951,
        "bandeira": "https://flags.restcountries.com/v5/w320/br.png",
    }


def test_cadastrar_favorito(cliente):
    resposta = cliente.post(
        "/api/favoritos",
        json=criar_pais(),
    )

    assert resposta.status_code == 201

    resposta_lista = cliente.get("/api/favoritos")
    favoritos = resposta_lista.get_json()

    assert len(favoritos) == 1
    assert favoritos[0]["nome"] == "Brazil"


def test_listar_favoritos_vazios(cliente):
    resposta = cliente.get("/api/favoritos")

    assert resposta.status_code == 200
    assert resposta.get_json() == []


def test_remover_favorito(cliente):
    cliente.post("/api/favoritos", json=criar_pais())

    resposta = cliente.delete("/api/favoritos/Brazil")

    assert resposta.status_code == 200
    assert cliente.get("/api/favoritos").get_json() == []


def test_rejeitar_favorito_invalido(cliente):
    resposta = cliente.post(
        "/api/favoritos",
        json={"nome": "Brazil"},
    )

    assert resposta.status_code == 400