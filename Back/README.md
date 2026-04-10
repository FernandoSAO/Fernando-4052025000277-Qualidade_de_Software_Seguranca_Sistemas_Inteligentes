# Back-end de Aprovação de Empréstimo com base no treinamento com machine learning do dataset Loan Approval Classification

link dataset: https://www.kaggle.com/datasets/taweilo/loan-approval-classification-data

Tem como funcionalidades:

    - obtém informações para preenchimento de campos dropdown para o frontend (URL: /getInformation  método: get);
    - inclusão de clientes ao banco de dados (URL: /registerClient  método: post);
    - verificação se cpf está na tabela de clientes (URL: /checkCPF  método: post);
    - inclusão de dados de empréstimo do cliente ao banco de dados com a verificação de aprovação utilizando o modelo treinado
    (URL: /registerLoanData  método: post);
    - obtém o histórico de testes de empréstimos feitos do banco de dados (URL: /getLoanHistory  método: get);
    - remove teste de empréstimo a partir do id do empréstimo (URL: /deleteLoan  método: delete);

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