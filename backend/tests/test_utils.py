from backend.utils import (
    validar_pesquisa,
    formatar_nome,
    extrair_informacoes_pais
)


def test_rejeita_pesquisa_vazia():
    assert validar_pesquisa("") is False

def test_aceita_pesquisa_valida():
    assert validar_pesquisa("Brasil") is True


def test_formata_nome():
    assert formatar_nome("  brasil  ") == "Brasil"


def test_extrai_informacoes_pais():
    dados = {
        "names": {"common": "Brazil"},
        "capitals": [
            {
                "name": "Brasília"
            }
        ],
        "population": 214211951,
        "codes": {
            "alpha_2": "BR"
        }
    }

    resultado = extrair_informacoes_pais(dados)

    assert resultado["nome"] == "Brazil"
    assert resultado["capital"] == "Brasília"
    assert resultado["populacao"] == 214211951
    assert resultado["bandeira"] == (
        "https://flags.restcountries.com/v5/w320/br.png"
    )