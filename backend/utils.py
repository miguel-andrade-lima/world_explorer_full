def validar_pesquisa(nome):
    return bool(nome and nome.strip())


def formatar_nome(nome):
    if not nome:
        return ""

    return nome.strip().title()


def extrair_informacoes_pais(dados):
    if not isinstance(dados, dict):
        return None

    nome = dados.get("names", {}).get("common")

    if not nome:
        return None

    capitais = dados.get("capitals") or []

    if capitais and isinstance(capitais[0], dict):
        capital = capitais[0].get("name", "Não informada")
    elif capitais:
        capital = capitais[0]
    else:
        capital = "Não informada"

    codigo = dados.get("codes", {}).get("alpha_2", "")

    bandeira = (
        f"https://flags.restcountries.com/v5/w320/{codigo.lower()}.png"
        if codigo
        else ""
    )

    return {
        "nome": nome,
        "capital": capital,
        "populacao": dados.get("population", 0),
        "bandeira": bandeira
    }