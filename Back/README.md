# API de Análise de Crédito com Machine Learning

**Dataset:** https://www.kaggle.com/datasets/taweilo/loan-approval-classification-data

---

## Sobre a API

Esta API é responsável por realizar a **análise de crédito para empréstimos**, combinando:

* **Regras de negócio**
* **Modelo de Machine Learning (CART)**

Ela permite **cadastrar clientes, simular empréstimos e consultar histórico**, retornando decisões de crédito em tempo real.

---

## Endpoints

| Método     | Endpoint            | Descrição                                          |
| ---------- | ------------------- | -------------------------------------------------- |
| **GET**    | `/getInformation`   | Dados para dropdowns (educação, moradia, objetivo) |
| **POST**   | `/registerClient`   | Cadastro de novo cliente                           |
| **POST**   | `/checkCPF`         | Verifica se o CPF já existe                        |
| **POST**   | `/registerLoanData` | Registra empréstimo e retorna análise do modelo    |
| **GET**    | `/getLoanHistory`   | Lista histórico de simulações                      |
| **DELETE** | `/deleteLoan`       | Remove empréstimo por ID                           |

---

## Regra de Negócio Importante

* Clientes com **inadimplência anterior (`previous_default`)** são automaticamente **negados**
* O modelo de ML **não é executado nesses casos**

---

## Tecnologias

### Backend

* Python 3.10 *(obrigatório)*
* Flask
* SQLite
* SQLAlchemy
* Pydantic
* Joblib

### Machine Learning

* Scikit-learn *(Decision Tree - CART)*
* Pandas / NumPy
* MinMaxScaler

### Testes

* Pytest
* Pytest-cov

---

# API de Análise de Crédito com Machine Learning

**Dataset:** https://www.kaggle.com/datasets/taweilo/loan-approval-classification-data

---

## Como Executar

### Pré-requisitos

* Python **3.10**
* pip

---

### Verificar versão do Python

```bash
python --version
```

---

### Instalar Python 3.10 (se necessário)

**Windows**

Baixe o instalador oficial do Python 3.10:  
https://www.python.org/downloads/release/python-31011/

> ⚠️ Durante a instalação, marque a opção **"Add Python to PATH"**

**Linux**

```bash
sudo apt install python3.10
```

**macOS**

```bash
brew install python@3.10
```

---

## Instalação

### 1. Acessar o diretório

```bash
cd Sprint\ 4/MVP/Back
```

---

### 2. Criar ambiente virtual

```bash
python -m venv venv
```

---

### 3. Ativar ambiente virtual

**Windows (PowerShell)**

```bash
.\venv\Scripts\activate
```

**Windows (CMD)**

```bash
venv\Scripts\activate.bat
```

**Linux/macOS**

```bash
source venv/bin/activate
```

---

### 4. Confirmar versão correta

```bash
python --version
```

---

### 5. Instalar dependências

```bash
pip install -r requirements.txt
```

---

## Executar a API

### Produção

```bash
flask run --host 0.0.0.0 --port 5000
```

---

### Desenvolvimento (com reload automático)

```bash
flask run --host 0.0.0.0 --port 5000 --reload
```

---

### Acessar documentação

```bash
http://localhost:5000/openapi/swagger
```

---

## Testes

### Rodar todos os testes

```bash
pytest tests/ -v
```

---

### Testes específicos

```bash
pytest tests/test_model_accuracy.py -v
```

```bash
pytest tests/test_model_mock.py -v
```

---

### Cobertura no terminal

```bash
pytest tests/ -v --cov=services --cov-report=term
```

---

### Cobertura em HTML

```bash
pytest tests/ -v --cov=services --cov-report=html
```

---

## Observações

* O projeto **depende especificamente do Python 3.10**
* O modelo já está treinado e pronto para uso (`.pkl`)
* O banco SQLite é criado automaticamente na primeira execução

## Estrutura do Projeto

```bash
Back/
├── app.py                     # API Flask
├── model/                     # Modelos SQLAlchemy
│   ├── base.py
│   ├── client.py
│   └── loan_data.py
│
├── schemas.py                 # Validação (Pydantic)
│
├── services/                  # Regras de negócio
│   └── loan_predictor.py
│
├── ml_model/                  # Modelo ML
│   ├── modelo_completo_cart.pkl
│   └── modelo_metadata.json
│
├── database/
│   └── db.sqlite3
│
├── tests/
│   ├── fixtures/
│   ├── test_conversions.py
│   ├── test_model_accuracy.py
│   ├── test_model_import.py
│   └── test_model_mock.py
│
├── requirements.txt
└── .gitignore
```
---

## Licença

MIT License

---

## Autor - Fernando Oliveira

Projeto desenvolvido para fins acadêmicos (PUC-RJ)
