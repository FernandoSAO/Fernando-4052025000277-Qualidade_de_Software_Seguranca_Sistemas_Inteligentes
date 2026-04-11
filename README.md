# Sistema de Análise de Crédito para Empréstimos com Machine Learning

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-2.3.3-green)](https://flask.palletsprojects.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Dataset:** [Loan Approval Classification Dataset](https://www.kaggle.com/datasets/taweilo/loan-approval-classification-data)

**Status do Projeto:** ✅ Concluído

**Instituição:** PUC-RJ | Pós-Graduação em Engenharia de Software  
**Disciplina:** Qualidade de Software, Segurança e Sistemas Inteligentes
""Link do Vídeo de Apresentação:** https://youtu.be/Zrq2sZ8K2Yc 

---

## 📖 Visão Geral do Projeto

Este projeto é um **MVP (Produto Mínimo Viável)** de um sistema de análise de crédito. O objetivo é automatizar a decisão de aprovação ou rejeição de pedidos de empréstimo, combinando **regras de negócio** com um **modelo de Machine Learning** treinado a partir do dataset *Loan Approval Classification Dataset*.

O projeto está dividido em três partes principais:

1.  **🔬 Análise e Treinamento (Google Colab):** Notebook interativo com toda a etapa de exploração, tratamento de dados, treinamento de múltiplos modelos e escolha do melhor.
2.  **⚙️ Backend (Python + Flask):** API RESTful responsável por gerenciar os dados (clientes, empréstimos) e hospedar o modelo de ML treinado para fazer as predições.
3.  **🖥️ Frontend (HTML, CSS, JS):** Interface web amigável para usuários realizarem cadastros, simulações de crédito e consultarem o histórico.

---

## 🎯 Funcionalidades do Sistema

### Aplicação Web (Frontend + Backend)
- **Cadastro de Clientes:** Registra informações pessoais (CPF, nome, data de nascimento) e financeiras (renda, score de crédito, experiência profissional, etc.).
- **Verificação de CPF:** Antes de cadastrar ou simular um empréstimo, o sistema verifica se o CPF já existe no banco de dados, evitando duplicidades.
- **Simulação de Empréstimo:** Usuário solicita um valor e informa os dados da operação. O sistema retorna a decisão (Aprovado/Negado) em tempo real.
- **Histórico de Transações:** Exibe uma tabela com todas as simulações de empréstimo já realizadas, permitindo visualizar datas, valores e resultados.
- **Regra de Negócio:** Implementada diretamente no backend: clientes com histórico de inadimplência (`default` anterior) são **automaticamente negados**, sem necessidade de consulta ao modelo de ML.
- **API RESTful:** Endpoints bem definidos para integração com outros sistemas ou futuros aplicativos.

### Análise e Modelagem de Dados (Google Colab)
- **Tratamento de Dados:** Remoção de vazamento de dados (*data leakage*) por feature determinística (`previous_default`).
- **Pré-processamento:** Aplicação de `Label Encoding` e `One-Hot Encoding` para transformar variáveis categóricas.
- **Comparação de Modelos:** Avaliação do desempenho base de quatro algoritmos: **KNN**, **CART (Árvore de Decisão)**, **Naive Bayes (NB)** e **SVM**.
- **Escalonamento de Dados:** Teste com `StandardScaler` (padronização) e `MinMaxScaler` (normalização) para identificar a melhor abordagem para cada modelo.
- **Otimização de Hiperparâmetros:** Busca pelos melhores parâmetros para os modelos **KNN**, **CART** e **Naive Bayes** (o SVM foi excluído da otimização devido ao seu alto custo computacional).
- **Seleção do Melhor Modelo:** O modelo escolhido para produção foi o **CART normalizado (`MinMaxScaler`)**, com os parâmetros:
    - `criterion`: `entropy`
    - `max_depth`: `10`
    - `min_samples_split`: `5`
- **Exportação do Modelo:** O modelo final (treinado com 100% dos dados), juntamente com o `scaler` e metadados, foi serializado usando a biblioteca `joblib` em um único arquivo `.pkl`, pronto para ser consumido pelo backend.

---

## 🛠️ Tecnologias Utilizadas

### Machine Learning (Google Colab)
- **Python 3.10**
- **Pandas, NumPy** (Manipulação de dados)
- **Scikit-learn** (Modelos, pré-processamento, métricas)
- **Joblib** (Exportação do modelo)

### Backend
- **Python 3.10**
- **Flask** (Framework web para a API)
- **SQLite** (Banco de dados relacional)
- **SQLAlchemy** (ORM para interação com o banco)
- **Pydantic** (Validação de dados)

### Frontend
- **HTML5, CSS3**
- **JavaScript (ES6+)**
- **Fetch API** (Comunicação com o backend)

### Testes e Qualidade
- **Pytest** (Testes unitários e de integração no backend)

---

## 📂 Estrutura do Projeto

```bash
.
├── Back/                          # Backend da aplicação
│   ├── app.py                     # Arquivo principal da API Flask
│   ├── model/                     # Modelos SQLAlchemy (Client, LoanData, LoanPredictor)
│   ├── schemas.py                 # Schemas Pydantic para validação
│   ├── ml_model/                  # Modelo de ML treinado (.pkl) e metadados
│   ├── tests/                     # Testes unitários e de integração (pytest)
│   └── requirements.txt           # Dependências do projeto Python
├── Front/                         # Frontend da aplicação
│   ├── index.html                 # Página principal
│   ├── css/                       # Componentes HTML (header e sidebar)
│   ├── css/                       # Estilos CSS
│   ├── js/                        # Arquivos JavaScript modulares
│   └── pages/                     # Páginas HTML
├── Analise_ML/                    # (Recomendado) Notebook do Google Colab
│   └── loan_analysis.ipynb        # Análise, treinamento e exportação do modelo
└── README.md                      # Documentação do projeto
