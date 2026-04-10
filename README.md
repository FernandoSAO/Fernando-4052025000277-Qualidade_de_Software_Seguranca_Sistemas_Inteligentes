# Repositório com o projeto de Aprovação de Empréstimo, com base no treinamento com machine learning do dataset Loan Approval Classification
PUC-RJ Pós Graduação em Engenharia de Software
Qualidade de Software, Segurança e Sistemas Inteligentes

link dataset: https://www.kaggle.com/datasets/taweilo/loan-approval-classification-data

Tem como funcionalidades:

    - obtém informações para preenchimento de campos dropdown para o frontend (URL: /getInformation  método: get);
    - inclusão de clientes ao banco de dados (URL: /registerClient  método: post);
    - verificação se cpf está na tabela de clientes (URL: /checkCPF  método: post);
    - inclusão de dados de empréstimo do cliente ao banco de dados com a verificação de aprovação utilizando o modelo treinado
    (URL: /registerLoanData  método: post);
    - obtém o histórico de testes de empréstimos feitos do banco de dados (URL: /getLoanHistory  método: get);
    - remove teste de empréstimo a partir do id do empréstimo (URL: /deleteLoan  método: delete);

O backend do sitema foi contruído em python utilizando como base dados o SQLite e mircoframework flask.
O frontend do sistema foi construído utilizando HTML, CSS e JavaScript
O treinamento do modelo foi feito utilizando o google collab em python utilizando o método de classificação com os modelos KNN, CART, NB e SVM

# Sistema de Análise de Crédito para Empréstimos com base no treinamento de dataset com machine learning

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-2.3.3-green)](https://flask.palletsprojects.com/)

link dataset: https://www.kaggle.com/datasets/taweilo/loan-approval-classification-data

**Status do Projeto:** ✅ Concluído

## 📖 Visão Geral

Este projeto é um MVP (Produto Mínimo Viável) de um sistema de análise de crédito. O objetivo é automatizar a decisão de aprovação ou rejeição de pedidos de empréstimo, combinando regras de negócio com um modelo de Machine Learning, com base no aprendizado
do dataset Loan Approval Classification Dataset

O sistema é composto por:
- **Backend**: Uma API RESTful desenvolvida em Flask que gerencia clientes, solicitações de empréstimo e hospeda o modelo de ML.
- **Frontend**: Uma interface web para cadastro de clientes, simulação de empréstimos e visualização do histórico.
- **Arquivo do Google Collab com os testes e treinamentos utilizando machine learnig**: Contem a Remoção de vazamento de dados por feature determinística, Label Encoding e One-Hot Encoding, Comparação dos modelos Pré e Pós Otimização dos HiperparÂmetros, detalhes
  do modelo escolhido e testes finais
- **Link vídeo do youtube com apresentação do projeto: (link)

## 🎯 Funcionalidades Principais

*   **Cadastro de Clientes**: Registra informações pessoais (CPF, nome, etc.) e financeiras (renda, score, etc.).
*   **Simulação de Empréstimo**: Permite solicitar um empréstimo e obtém uma decisão (Aprovado/Negado) em tempo real com base no modelo e em regras de negócio.
*   **Histórico de Transações**: Exibe uma tabela com todas as simulações de empréstimo já realizadas.
*   **Verificação de cpf no sistema**: Verifica se cpf já foi registrado para evitar preenchimento desnecessário de cliente para cpf repetidos ou a falta do cpf para registro do empréstimo
*   **Regra de Negócio**: Clientes com `default` (inadimplência) anterior são automaticamente negados.
*   **API RESTful**: Endpoints documentados para integração com outros sistemas.

## 🛠️ Tecnologias Utilizadas

### Backend
*   **Python 3.10**
*   **Flask** - Framework web para a API.
*   **SQLite** - Banco de dados SQLite.

# Frontend
*   **HTML5, CSS3 e JavaScript (ES6+)**
*   **Fetch API** - Para comunicação com o backend.

### Machine Learning
*   **Modelos Utilizados** - `KNN`, `CART`, `Naive Bayes` e `SVM`.
*   **Otimizações** - Paronização e Normalização
*   **Otimização dos hiperparâmetros** - `KNN`, `CART` e `Naive Bayes` (Pelo fato do SVM demorar muito tempo, foi o único que não teve otimização)
*   **Escolha do melhor modelo e sua exportação para uso na APP** - `CART`



### Testes
*   **Pytest** - Framework para testes unitários e de integração.

## 📂 Estrutura do Projeto

```bash
.
├── Back/
│   ├── app.py                  # Arquivo principal da aplicação Flask
│   ├── model/                  # Modelos SQLAlchemy (Client, LoanData)
│   ├── schemas.py              # Schemas Pydantic para validação
│   ├── services/               # Lógica de negócio (LoanPredictor)
│   ├── ml_model/               # Modelo de ML treinado (.pkl) e metadados
│   ├── tests/                  # Testes unitários e de integração (pytest)
│   └── requirements.txt        # Dependências do projeto Python
├── Front/                      # Arquivos estáticos do frontend (HTML, CSS, JS)
└── README.md                   # Documentação do projeto
