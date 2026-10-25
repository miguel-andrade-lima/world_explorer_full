import os
from pathlib import Path

import requests
from flask import Flask, jsonify, request, send_from_directory

from backend.utils import validar_pesquisa, extrair_informacoes_pais

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"

app = Flask(
    __name__,
    static_folder=str(FRONTEND_DIR),
    static_url_path="/static"
)

@app.route("/")
def inicio():
    return send_from_directory(str(FRONTEND_DIR), "index.html")


@app.route("/static/<path:arquivo>")
def arquivos_estaticos(arquivo):
    return send_from_directory(str(FRONTEND_DIR), arquivo)


@app.route("/api/paises")
def buscar_paises():
    nome = request.args.get("nome", "").strip()

    if not validar_pesquisa(nome):
        return jsonify({
            "erro": "Informe o nome de um país."
        }), 400

    chave_api = os.getenv("RESTCOUNTRIES_API_KEY")

    if not chave_api:
        return jsonify({
            "erro": "A chave da API não foi configurada."
        }), 500

    url = "https://api.restcountries.com/countries/v5/name"

    try:
        resposta = requests.get(
            url,
            params={"q": nome},
            headers={
                "Authorization": f"Bearer {chave_api}"
            },
            timeout=15
        )

        resposta.raise_for_status()
        resultado = resposta.json()

        dados = resultado.get("data", {}).get("objects", [])

        paises = [
            extrair_informacoes_pais(pais)
            for pais in dados
        ]

        paises = [
            pais for pais in paises
            if pais is not None
        ]

        if not paises:
            return jsonify({
                "erro": "Nenhum país encontrado."
            }), 404

        return jsonify(paises)

    except requests.RequestException:
        return jsonify({
            "erro": "Não foi possível consultar a API de países."
        }), 502

    except (ValueError, AttributeError):
        return jsonify({
            "erro": "A API retornou uma resposta inválida."
        }), 502


if __name__ == "__main__":
    app.run(debug=True)