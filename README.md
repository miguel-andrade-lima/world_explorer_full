World Explorer 

Aplicação web para pesquisar países e gerenciar uma lista de favoritos. O projeto foi desenvolvido em Python, com interface web, integração com uma API externa e armazenamento de dados em SQLite.

Repositório: https://github.com/miguel-andrade-lima/world_explorer_full

Docker Hub: https://hub.docker.com/r/miguelandradelima/world-explorer

1. Integrante e responsabilidades

Nome - Miguel Andrade de Lima

Matrícula - 22505921

GitHub - miguel-andrade-lima

Responsabilidade - Desenvolvimento da aplicação, backend Python, frontend, banco de dados, testes automatizados e Docker

PR principal

O projeto foi desenvolvido individualmente. A atividade original prevê trabalho em grupo e revisão por outro integrante, mas não havia pessoas na turma fazendo a mesma disciplina

2. Descrição da aplicação

O World Explorer permite pesquisar países e consultar suas informações, além de salvar, listar e excluir países favoritos.

Funcionalidades

Pesquisa de países por nome.

Consulta de informações por meio de uma API externa.

Exibição de informações dos países, incluindo nome, capital, população e bandeira.

Cadastro, listagem e exclusão de favoritos.

Validação dos dados recebidos pelo backend.

Interface web integrada ao backend Python.

Tecnologias utilizadas

Frontend: HTML, CSS e JavaScript.

Backend: Python e Flask.

Banco de dados: SQLite.

API externa: Rest Countries, utilizada para consultar informações dos países.

Testes: pytest.

Integração contínua: GitHub Actions.

Containerização: Docker.

Publicação da imagem: Docker Hub.

Banco de dados

O SQLite armazena os países favoritos em uma tabela chamada favoritos, com os campos id, nome, capital, populacao e bandeira.

API externa

A aplicação consulta a API de países utilizando a variável de ambiente RESTCOUNTRIES_API_KEY. A chave é enviada no cabeçalho de autorização da requisição.

A chave não deve ser inserida diretamente no código-fonte nem publicada no repositório.

3. Como executar localmente

Pré-requisitos

Python 3.12 ou compatível.

Git.

Uma chave válida para a API externa.

Instalação

Clone o repositório:

git clone https://github.com/miguel-andrade-lima/world_explorer_full.git
cd world_explorer_full

Crie e ative um ambiente virtual no Windows PowerShell:

python -m venv .venv
.\.venv\Scripts\Activate.ps1

Instale as dependências:

pip install -r backend/requirements.txt

Configure a chave da API no PowerShell, substituindo o valor pelo seu próprio token:

$env:RESTCOUNTRIES_API_KEY="SUA_CHAVE_API"

Inicie a aplicação:

python -m flask --app backend.app run --debug

Acesse no navegador:

http://127.0.0.1:5000

O banco de dados SQLite é criado automaticamente pela aplicação.

4. Como executar com Docker

Imagem publicada: miguelandradelima/world-explorer

Tag disponível: latest

Com o Docker instalado, execute:

docker pull miguelandradelima/world-explorer:latest

Inicie o contêiner:

docker run -d --name world-explorer -p 8080:5000 -e RESTCOUNTRIES_API_KEY=SUA_CHAVE_API miguelandradelima/world-explorer:latest

Substitua SUA_CHAVE_API pela chave válida da API.

Acesse a aplicação em:

http://localhost:8080

Para consultar os logs:

docker logs world-explorer

Para parar o contêiner:

docker stop world-explorer

Para removê-lo:

docker rm world-explorer

Observação: o banco SQLite é armazenado no sistema de arquivos do contêiner. Para manter os favoritos após remover o contêiner, é necessário configurar um volume persistente.

5. Testes automatizados

O projeto utiliza pytest para verificar as funções centrais da aplicação.

Os testes cobrem:

Validação de pesquisas vazias e válidas.

Formatação de nomes de países.

Extração de informações dos países.

Cadastro, listagem e exclusão de favoritos.

Rejeição de dados inválidos.

Para executar os testes a partir da raiz do projeto:

python -m pytest backend/tests -v

Resultado validado localmente: 8 testes passaram.

Integração contínua

O workflow está em .github/workflows/ci.yml e é executado em eventos de push para a main e de Pull Request direcionada à main.

O GitHub Actions instala as dependências Python e executa a suíte de testes. O check de testes também foi selecionado na regra de proteção da branch principal.

6. Evidências do GitHub Actions

Teste de falha

Foi criada uma alteração temporária em um teste para provocar uma falha intencional. A Pull Request de teste apresentou falha no GitHub Actions.

Captura de tela: adicionar em docs/evidencias/ci-falha-pr.png.



Correção do teste

A alteração foi revertida e os testes foram executados novamente. O resultado local foi de 8 testes aprovados, e a execução da Pull Request voltou a ficar verde.

Observação: a falha demonstra que o CI detectou um teste quebrado. Para comprovar visualmente o bloqueio do merge pela regra de proteção, é necessário registrar também o estado da Pull Request com o check obrigatório reprovado.

7. Pull Requests e colaboração

O repositório possui uma regra de proteção para a branch main, exigindo Pull Request, uma aprovação e aprovação dos checks obrigatórios.

A Pull Request criada para demonstrar a falha do CI deve ser registrada como evidência técnica, e não como PR de funcionalidade.

PR de teste do CI: https://github.com/miguel-andrade-lima/world_explorer_full/pulls

A revisão por outro integrante e a aprovação de uma PR de funcionalidade ainda precisam ser realizadas conforme as regras da atividade, ou tratadas com o professor caso seja autorizada a entrega individual.

8. Conflitos de merge

Até o momento, não foi registrado um conflito de merge resolvido durante o fluxo descrito neste documento. Caso ocorra um conflito, o README deverá ser atualizado com a causa, os arquivos envolvidos, a forma de resolução e a validação realizada após a correção.

9. Publicação

O código-fonte está disponível no GitHub:

https://github.com/miguel-andrade-lima/world_explorer_full

A imagem Docker está disponível no Docker Hub:

https://hub.docker.com/r/miguelandradelima/world-explorer

O projeto utiliza testes automatizados e publicação de imagem por workflows do GitHub Actions.