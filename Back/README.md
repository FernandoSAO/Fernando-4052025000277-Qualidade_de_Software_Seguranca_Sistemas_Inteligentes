# API de inclusão de faturas e empresas

Esta API tem como objetivo a gestão de faturas de recebimento e pagamento.

Tem como funcionalidades:

    - inclusão de faturas de pagamento (URL: /addPaymentInvoice  método: post);
    - inclusão de faturas de recebimento (URL: /addReceiptInvoice  método: post);
    - inclusão de empresas (URL: /addCompany  método: post);
    - busca de logradouro, bairro e UF a partir do CEP, utilizando a API dos Correios (ViaCEP) (URL: /getCEPInformation  método: get);
    - busca por faturas de pagamento a partir de um sistema de filtros (URL: /getPaymentInvoicesByFilters  método: get);
    - busca por faturas de recebimento a partir de um sistema de filtros (URL: /getReceiptInvoicesByFilters  método: get);
    - busca por empresas a partir de um sistema de filtros (URL: /getCompaniesByFilters  método: get);
    - alteração do estado de faturas de pagamento (aberto -> fechado) (URL: /markPaymentInvoicePaid  método: patch);
    - alteração do estado de faturas de recebimento (aberto -> fechado) (URL: /markReceiptInvoicePaid  método: patch);
    - exclusão de faturas de pagamento (URL: /deletePaymentInvoice  método: delete);
    - exclusão de faturas de recebimento (URL: /deleteReceiptInvoice  método: delete);
    - exclusão de empresas (URL: /deleteCompany  método: delete);

O sitema foi contruído em python utilizando como base dados o SQLite e mircoframework flask.

---

## Como executar 

Será necessário ter todas as libs python listadas no `requirements.txt` instaladas.
Após clonar o repositório, é necessário ir ao diretório raiz, pelo terminal, para poder executar os comandos descritos abaixo.

> É fortemente indicado o uso de ambientes virtuais do tipo [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html).

```
venv\Scripts\activate
```

```
(env)$ pip install -r requirements.txt
```

Este comando instala as dependências/bibliotecas, descritas no arquivo `requirements.txt`.

Para executar a API  basta executar:

```
(env)$ flask run --host 0.0.0.0 --port 5000
```

Em modo de desenvolvimento é recomendado executar utilizando o parâmetro reload, que reiniciará o servidor
automaticamente após uma mudança no código fonte. 

```
(env)$ flask run --host 0.0.0.0 --port 5000 --reload
```

Abra o [http://localhost:5000/#/](http://localhost:5000/#/) no navegador para verificar o status da API em execução.

---
## Como executar através do Docker

Certifique-se de ter o [Docker](https://docs.docker.com/engine/install/) instalado e em execução em sua máquina.

Navegue até o diretório que contém o Dockerfile e o requirements.txt no terminal.
Execute **como administrador** o seguinte comando para construir a imagem Docker:

```
$ docker build -t rest-api .
```

Uma vez criada a imagem, para executar o container basta executar, **como administrador**, seguinte o comando:

```
$ docker run -p 5000:5000 rest-api
```

Uma vez executando, para acessar a API, basta abrir o [http://localhost:5000/#/](http://localhost:5000/#/) no navegador.


### Alguns comandos úteis do Docker

>**Para verificar se a imagem foi criada** você pode executar o seguinte comando:
>
>```
>$ docker images
>```
>
> Caso queira **remover uma imagem**, basta executar o comando:
>```
>$ docker rmi <IMAGE ID>
>```
>Subistituindo o `IMAGE ID` pelo código da imagem
>
>**Para verificar se o container está em exceução** você pode executar o seguinte comando:
>
>```
>$ docker container ls --all
>```
>
> Caso queira **parar um conatiner**, basta executar o comando:
>```
>$ docker stop <CONTAINER ID>
>```
>Subistituindo o `CONTAINER ID` pelo ID do conatiner
>
>
> Caso queira **destruir um conatiner**, basta executar o comando:
>```
>$ docker rm <CONTAINER ID>
>```
>Para mais comandos, veja a [documentação do docker](https://docs.docker.com/engine/reference/run/).
