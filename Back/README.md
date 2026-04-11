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

## Como Executar

### Pré-requisitos

* Python **3.10**
* pip

---

### Verificar versão do Python (esperado Python 3.10)

```bash
python --version
```

Caso necessário:

* Windows: https://www.python.org/downloads/release/python-31011/
* Linux:

```bash
sudo apt install python3.10
```

* macOS:

```bash
brew install python@3.10
```

---

### 📦 Instalação

```bash
# Entrar no diretório do backend
cd Sprint\ 4/MVP/Back

# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual

# Windows (PowerShell)
.\venv\Scripts\activate

# Windows (CMD)
venv\Scripts\activate.bat

# Linux/macOS
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

---

### ▶️ Executar a API

```bash
# Produção
flask run --host 0.0.0.0 --port 5000

# Desenvolvimento (recomendado)
flask run --host 0.0.0.0 --port 5000 --reload
```

🔗 Acesse a documentação:

```
http://localhost:5000/openapi/swagger
```

---

## 🧪 Testes

```bash
# Rodar todos os testes
pytest tests/ -v

# Testes específicos
pytest tests/test_model_accuracy.py -v
pytest tests/test_model_mock.py -v

# Cobertura (terminal)
pytest tests/ -v --cov=services --cov-report=term

# Cobertura (HTML)
pytest tests/ -v --cov=services --cov-report=html
```

---

## 📂 Estrutura do Projeto

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

## ⚡ Observações

* ⚠️ O projeto **depende especificamente do Python 3.10**
* 📦 O modelo já está treinado e pronto para uso (`.pkl`)
* 🔄 O banco SQLite é criado automaticamente na primeira execução

---

## 📄 Licença

MIT License

---

## 👨‍💻 Autor

Projeto desenvolvido para fins acadêmicos (PUC-RJ)
