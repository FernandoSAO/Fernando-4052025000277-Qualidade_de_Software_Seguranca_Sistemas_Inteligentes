# Front-end de Aprovação de Empréstimo com base no treinamento com machine learning do dataset Loan Approval Classification

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

Recomendado o uso de ferramentas como o Go Live do Vscode 