const formulario = document.getElementById("form-pesquisa");
const campoNome = document.getElementById("nome-pais");
const resultados = document.getElementById("resultados");
const mensagem = document.getElementById("mensagem");

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
        const resposta = await fetch(
            `/api/paises?nome=${encodeURIComponent(nome)}`
        );

        const dados = await resposta.json();

        if (!resposta.ok) {
            throw new Error(dados.erro || "Não foi possível pesquisar.");
        }

        if (dados.length === 0) {
            mensagem.textContent = "Nenhum país encontrado.";
            return;
        }

        mensagem.textContent = `${dados.length} país(es) encontrado(s).`;

        dados.forEach((pais) => {
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

            cartao.append(bandeira, titulo, capital, populacao);
            resultados.appendChild(cartao);
        });
    } catch (erro) {
        mensagem.textContent = erro.message;
    }
});