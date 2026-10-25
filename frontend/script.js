const formulario = document.getElementById("form-pesquisa");
const campoNome = document.getElementById("nome-pais");
const resultados = document.getElementById("resultados");
const mensagem = document.getElementById("mensagem");

// Cria o botão e a área de favoritos sem precisar alterar o HTML.
const botaoVerFavoritos = document.createElement("button");
botaoVerFavoritos.type = "button";
botaoVerFavoritos.textContent = "Ver favoritos";
botaoVerFavoritos.className = "botao-favorito";

const areaFavoritos = document.createElement("section");
areaFavoritos.hidden = true;

const tituloFavoritos = document.createElement("h2");
tituloFavoritos.textContent = "Meus países favoritos";

const listaFavoritos = document.createElement("div");
listaFavoritos.id = "lista-favoritos";

areaFavoritos.append(tituloFavoritos, listaFavoritos);
formulario.insertAdjacentElement("afterend", botaoVerFavoritos);
botaoVerFavoritos.insertAdjacentElement("afterend", areaFavoritos);

async function requisicaoJson(url, opcoes = {}) {
    const resposta = await fetch(url, opcoes);
    const dados = await resposta.json();

    if (!resposta.ok) {
        throw new Error(
            dados.erro || dados.mensagem || "Ocorreu um erro."
        );
    }

    return dados;
}

function criarCartao(pais, tipo = "pesquisa") {
    const cartao = document.createElement("article");
    cartao.className = "pais";

    const bandeira = document.createElement("img");
    bandeira.src = pais.bandeira;
    bandeira.alt = `Bandeira de ${pais.nome}`;
    bandeira.loading = "lazy";

    const titulo = document.createElement("h3");
    titulo.textContent = pais.nome;

    const capital = document.createElement("p");
    capital.textContent = `Capital: ${pais.capital}`;

    const populacao = document.createElement("p");
    populacao.textContent =
        `População: ${Number(pais.populacao).toLocaleString("pt-BR")}`;

    const botao = document.createElement("button");
    botao.type = "button";

    if (tipo === "favorito") {
        botao.textContent = "Remover favorito";
        botao.addEventListener("click", async () => {
            try {
                await requisicaoJson(
                    `/api/favoritos/${encodeURIComponent(pais.nome)}`,
                    { method: "DELETE" }
                );

                await carregarFavoritos();
                mensagem.textContent =
                    `${pais.nome} foi removido dos favoritos.`;
            } catch (erro) {
                mensagem.textContent = erro.message;
            }
        });
    } else {
        botao.textContent = "Adicionar aos favoritos";
        botao.addEventListener("click", async () => {
            try {
                const resposta = await requisicaoJson(
                    "/api/favoritos",
                    {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json"
                        },
                        body: JSON.stringify(pais)
                    }
                );

                mensagem.textContent = resposta.mensagem;
            } catch (erro) {
                mensagem.textContent = erro.message;
            }
        });
    }

    cartao.append(
        bandeira,
        titulo,
        capital,
        populacao,
        botao
    );

    return cartao;
}

// Pesquisa países pela API externa através do Flask.
formulario.addEventListener("submit", async (evento) => {
    evento.preventDefault();

    const nome = campoNome.value.trim();
    resultados.replaceChildren();

    if (!nome) {
        mensagem.textContent = "Digite o nome de um país.";
        return;
    }

    mensagem.textContent = "Pesquisando países...";

    try {
        const dados = await requisicaoJson(
            `/api/paises?nome=${encodeURIComponent(nome)}`
        );

        if (!Array.isArray(dados) || dados.length === 0) {
            mensagem.textContent = "Nenhum país encontrado.";
            return;
        }

        dados.forEach((pais) => {
            resultados.appendChild(criarCartao(pais));
        });

        mensagem.textContent =
            `${dados.length} país(es) encontrado(s).`;
    } catch (erro) {
        mensagem.textContent = erro.message;
    }
});

// Carrega os países que estão salvos no SQLite.
async function carregarFavoritos() {
    listaFavoritos.replaceChildren();

    try {
        const favoritos = await requisicaoJson("/api/favoritos");

        if (favoritos.length === 0) {
            listaFavoritos.textContent =
                "Você ainda não tem países favoritos.";
            return;
        }

        favoritos.forEach((pais) => {
            listaFavoritos.appendChild(
                criarCartao(pais, "favorito")
            );
        });
    } catch (erro) {
        listaFavoritos.textContent = erro.message;
    }
}

// Mostra ou esconde a área de favoritos.
botaoVerFavoritos.addEventListener("click", async () => {
    areaFavoritos.hidden = !areaFavoritos.hidden;

    if (!areaFavoritos.hidden) {
        await carregarFavoritos();
    }

    botaoVerFavoritos.textContent = areaFavoritos.hidden
        ? "Ver favoritos"
        : "Ocultar favoritos";
});