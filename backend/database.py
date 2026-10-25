import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_PATH = BASE_DIR / "paises.db"


def conectar():
    conexao = sqlite3.connect(DATABASE_PATH)
    conexao.row_factory = sqlite3.Row
    return conexao


def criar_tabela():
    with conectar() as conexao:
        conexao.execute("""
            CREATE TABLE IF NOT EXISTS favoritos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL UNIQUE,
                capital TEXT NOT NULL,
                populacao INTEGER NOT NULL,
                bandeira TEXT NOT NULL
            )
        """)


def listar_favoritos():
    with conectar() as conexao:
        registros = conexao.execute(
            "SELECT nome, capital, populacao, bandeira "
            "FROM favoritos ORDER BY nome"
        ).fetchall()

        return [dict(registro) for registro in registros]


def adicionar_favorito(pais):
    with conectar() as conexao:
        conexao.execute(
            """
            INSERT INTO favoritos (nome, capital, populacao, bandeira)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(nome) DO NOTHING
            """,
            (
                pais["nome"],
                pais["capital"],
                pais["populacao"],
                pais["bandeira"],
            ),
        )


def remover_favorito(nome):
    with conectar() as conexao:
        cursor = conexao.execute(
            "DELETE FROM favoritos WHERE nome = ?",
            (nome,),
        )
        return cursor.rowcount > 0

if __name__ == "__main__":
    criar_tabela()
    print("Banco de dados criado com sucesso!")