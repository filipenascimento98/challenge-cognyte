# Desafio Técnico Cognyte

O objetivo deste desafio é criar um software para receber dados via rede e armazená-los em arquivos.

# Tecnologias
- [Python](https://www.python.org/)
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

# Configuração
No arquivo __.env__ é necessário configurar os valores de timeout, porta do servidor e tamanho máximo dos arquivos que são respectivamente as variáveis __TIMEOUT__, __PORT__ e __MAX_FILE_LENGTH__.

# Como executar
Para acessar o projeto basta clonar este respositório, instalar as tecnologias citadas acima e executar o seguinte comando
```bash
docker-compose up -d --build
```
Uma vez buildado a flag __--build__ não é mais necessária.

A flag __-d__ serve para rodar a aplicação e não ocupar o atual terminal, se preferir pode executar sem esta flag.
Com o servidor em execução conforme o passo anterior podemos interagir com ele por meio do arquivo __client.py__. Para executar o client, antes descubra o IP do container no qual está sendo executado o servidor com o comando:
```bash
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' <id_container>
```
O ID do container pode ser obtido com o comando:
```
docker ps
```
O container é aquele com nome __server__. O IP retornado deve ser substituído na variável __SERVER__ do arquivo __client.py__ e para executar crie um ambiente virtual, instale as dependências listadas no arquivo __requirements.txt__ no ambiente e execute o respectivo comando:
```bash
python client.py
```
Com isso o cliente entrará em execução e você conseguirá enviar mensagens para o servidor.